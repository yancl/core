from __future__ import absolute_import

import torndb
from zhwcore.common.rpc_proxy import RPCProxy
from zhwcore.utils.md5 import get_md5

mysql_clients = {}

class TorndbWrapper(torndb.Connection):
    def __init__(self, *args, **kwargs):
        super(TorndbWrapper, self).__init__(*args, **kwargs)

    def insert_dict(self, table, **kwargs):
        keys = ','.join(kwargs.keys())
        place_holder=','.join(['%s'] * len(kwargs))
        sql = 'insert into %(table)s(%(keys)s) values(%(values)s)' % {'table':table, 'keys':keys, 'values':place_holder}
        param = kwargs.values()
        return self.insert(sql, *param)

    def update_dict(self, table, pk, pk_name='id', **kwargs):
        place_holder = ','.join('{0}=%({0})s'.format(k) for k in kwargs.keys())
        static_param = {'table':table, 'pk_name':pk_name}
        sql = 'update %(table)s set {0} where %(pk_name)s={1}' % static_param
        sql = sql.format(place_holder, '%(pk_val)s')
        update_param = kwargs
        update_param['pk_val'] = pk
        return self.update(sql, **update_param)


def get_mysql_client(host, port, user, passwd, database, max_conn_num=30, **kwargs):
    s = str(host) + str(port) + str(user) + str(passwd) + str(database) + str(kwargs)
    key = get_md5(s)

    global mysql_clients
    if key not in mysql_clients:
        params = {'host': host, 'port': port, 'user':user, 'password':passwd, 'database':database}
        params.update(kwargs)
        #proxy = RPCProxy(cls=torndb.Connection, max_conn_num=max_conn_num, **params)
        proxy = RPCProxy(cls=TorndbWrapper, max_conn_num=max_conn_num, **params)
        mysql_clients[key] = proxy
    return mysql_clients[key]
