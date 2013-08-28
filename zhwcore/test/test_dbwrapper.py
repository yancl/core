from __future__ import absolute_import

from zhwcore.client.mysql_r import get_mysql_client
from zhwcore.client.dbwrapper import DBWrapper

class TestCaseDBWrapper(object):
    def __init__(self):
        self._host = '127.0.0.1'
        self._port = 3306
        self._user = 'root'
        self._passwd = None
        self._db = 'test'
        
    def setup(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        db_handler.execute('create table t(id int not null auto_increment primary key, name varchar(30));')

    def teardown(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        db_handler.execute('drop table t;')

    def test_insert(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        seq_id = db_handler.insert('t', **{'name': 'yancl'})
        rows = db_handler.where('t', id=seq_id)
        assert len(rows) == 1
        assert rows[0]['name'] == 'yancl'
        assert db_handler.delete('t', where='id=$id', vars={'id': seq_id}) == 1

    def test_update(self):
        CLIENT_FOUND_ROWS = 2
        kwargs = {'client_flag':CLIENT_FOUND_ROWS, 'charset':'utf8mb4'}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        rowcount = db_handler.update('t', where='name=$name', vars={'name': 'yancl'}, **{'name': 'yanclx'})
        assert rowcount == 0

        seq_id = db_handler.insert('t', **{'name': 'yancl'})

        rowcount = db_handler.update('t', where='id=$seq_id', vars={'seq_id': seq_id}, **{'name': 'yancl'})
        assert rowcount == 1

        rowcount = db_handler.update('t', where='id=$seq_id', vars={'seq_id': seq_id}, **{'name': 'yanclx'})
        assert rowcount == 1

        assert db_handler.delete('t', where='id=$seq_id', vars={'seq_id': seq_id}) == 1

    def test_select(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        rows = db_handler.select('t', where='id=$id', vars={'id': 0})
        assert len(rows) == 0

        seq_id = db_handler.insert('t', **{'name': 'yancl'})
        rows = db_handler.select('t', where='id=$seq_id', vars={'seq_id': seq_id})
        assert len(rows) == 1
        assert rows[0]['name'] == 'yancl'
        db_handler.delete('t', where='id=$seq_id', vars={'seq_id': seq_id})

    def test_where(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        rows = db_handler.where('t', id=0)
        assert len(rows) == 0

        seq_id = db_handler.insert('t', **{'name': 'yancl'})
        rows = db_handler.where('t', id=seq_id)
        assert len(rows) == 1
        assert rows[0]['name'] == 'yancl'
        db_handler.delete('t', where='id=$seq_id', vars={'seq_id': seq_id})

    def test_query(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        rows = db_handler.query('select * from t where id=$seq_id', vars={'seq_id': 0})
        assert len(rows) == 0

        seq_id = db_handler.insert('t', **{'name': 'yancl'})
        rows = db_handler.query('select * from t where id=$seq_id', vars={'seq_id': seq_id})
        assert len(rows) == 1
        assert rows[0]['name'] == 'yancl'
        db_handler.delete('t', where='id=$seq_id', vars={'seq_id': seq_id})

    def test_execute(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        db_handler.execute('create table t2(id int not null auto_increment primary key, name varchar(30));')
        db_handler.execute('drop table t2;')

    def test_multi_insert(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        db_handler = DBWrapper(c)
        seq_id = db_handler.multiple_insert('t', values=[{'name': 'yancl'}, {'name': 'yancl'}])
        rows = db_handler.where('t', name='yancl')
        assert len(rows) == 2
        assert rows[0]['name'] == 'yancl'
        assert rows[1]['name'] == 'yancl'
        assert db_handler.delete('t', where='name=$name', vars={'name': 'yancl'}) == 2
