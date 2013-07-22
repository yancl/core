from __future__ import absolute_import

import cmemcached

from zhwcore.common.rpc_proxy import RPCProxy
from zhwcore.utils.md5 import get_md5

mc_clients = {}

class MC(cmemcached.Client):
    def __init__(self, servers, comp_threshold, comp_method):
        super(MC, self).__init__(servers, comp_threshold, comp_method)
        self.set_behavior(cmemcached.BEHAVIOR_BINARY_PROTOCOL, 1)

def get_mc_client(servers, max_conn_num=30):
    sorted_servers = servers
    sorted_servers.sort()
    key = get_md5(''.join(sorted_servers))

    global mc_clients
    if key not in mc_clients:
        params = {'servers': servers, 'comp_threshold':256, 'comp_method':'quicklz'}
        proxy = RPCProxy(cls=MC, max_conn_num=max_conn_num, **params)
        mc_clients[key] = proxy
    return mc_clients[key]
