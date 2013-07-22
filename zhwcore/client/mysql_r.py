from __future__ import absolute_import

import torndb
from zhwcore.common.rpc_proxy import RPCProxy
from zhwcore.utils.md5 import get_md5

mysql_clients = {}

def get_mysql_client(host, port, user, passwd, database, max_conn_num=30, **kwargs):
    s = str(host) + str(port) + str(user) + str(passwd) + str(database) + str(kwargs)
    key = get_md5(s)

    global mysql_clients
    if key not in mysql_clients:
        params = {'host': host, 'port': port, 'user':user, 'password':passwd, 'database':database}
        params.update(kwargs)
        proxy = RPCProxy(cls=torndb.Connection, max_conn_num=max_conn_num, **params)
        mysql_clients[key] = proxy
    return mysql_clients[key]
