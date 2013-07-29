from __future__ import absolute_import

from zhwcore.client.mysql_r import get_mysql_client

class TestCaseMysqlClient(object):
    def __init__(self):
        self._host = '127.0.0.1'
        self._port = 3306
        self._user = 'root'
        self._passwd = None
        self._db = 'test'
        
    def setup(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        c.execute('create table t(id int not null auto_increment primary key, name varchar(30));')

    def teardown(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        c.execute('drop table t;')

    def test_factory(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        c2 = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        from zhwcore.client import mysql_r
        assert len(mysql_r.mysql_clients) == 1
        assert c == c2

        kwargs = {'charset':'utf8mb4'}
        c3 = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        assert len(mysql_r.mysql_clients) == 2
        assert c2 != c3

    def test_insert(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        seq_id = c.insert('insert into t(name) values(%(name)s)', **{'name':'yancl'})
        row = c.get('select * from t where id=%s', seq_id)
        assert row.name == 'yancl'
        assert c.execute_rowcount('delete from t where id=%s', seq_id) == 1

    def test_update(self):
        CLIENT_FOUND_ROWS = 2
        kwargs = {'client_flag':CLIENT_FOUND_ROWS, 'charset':'utf8mb4'}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        rowcount = c.update('update t set name=%(newname)s where name=%(oldname)s', **{'newname':'yanclx', 'oldname':'yancl'})
        assert rowcount == 0

        seq_id = c.insert('insert into t(name) values(%(name)s)', **{'name':'yancl'})
        rowcount = c.update('update t set name=%(newname)s where name=%(oldname)s', **{'newname':'yancl', 'oldname':'yancl'})
        assert rowcount == 1

        rowcount = c.update('update t set name=%(newname)s where name=%(oldname)s', **{'newname':'yanclx', 'oldname':'yancl'})
        assert rowcount == 1

        assert c.execute_rowcount('delete from t where id=%s', seq_id) == 1

    def test_insert_dict(self):
        kwargs = {}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        seq_id = c.insert_dict(table='t', **{'name':'yancl'})
        row = c.get('select * from t where id=%s', seq_id)
        assert row.name == 'yancl'
        row_x = c.get_row(table='t', what='name', pk=seq_id, pk_name='id')
        assert row_x.name == 'yancl'
        assert c.execute_rowcount('delete from t where id=%s', seq_id) == 1

    def test_update_dict(self):
        CLIENT_FOUND_ROWS = 2
        kwargs = {'client_flag':CLIENT_FOUND_ROWS, 'charset':'utf8mb4'}
        c = get_mysql_client(self._host, self._port, self._user, self._passwd, self._db, max_conn_num=30, **kwargs)
        rowcount = c.update_dict(table='t', pk_name='id', pk=1, **{'name':'aaa'})
        assert rowcount == 0
