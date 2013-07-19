import cmemcached

from common.rpc_proxy import RPCProxy
from utils.md5 import get_md5

mc_clients = {}

class MC(cmemcached.Client):
    def __init__(hosts, comp_threshold, comp_method):
        super(MC, self).__init__(hosts, comp_threshold, comp_method)
        self.set_behavior(cmemcached.BEHAVIOR_BINARY_PROTOCOL, 1)

def get_mc_client(hosts, max_conn_num=30):
    sorted_hosts = hosts
    key = get_md5(sorted_hosts)
    if key not in mc_clients:
        params = {'servers': hosts, 'comp_threshold':256, 'comp_method':'quicklz'}
        proxy = RPCProxy(cls=MC, max_conn_num=max_conn_num, **params)
        mc_clients[key] = proxy
    return mc_clients[key]
