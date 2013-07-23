from __future__ import absolute_import

from thrift_client import ThriftClient
from thrift.protocol import TBinaryProtocol
from zhwcore.common.rpc_proxy import TracedRPCProxy

thrift_clients = {}

def get_thrift_client(cls, hosts, excpt_classes=(), max_conn_num=30, retries=2, timeout=3, connect_timeout=0.5):
    '''
        there should be only one thrift client for each service in one process
        so we make it like a factory
    '''
    hosts_t = hosts
    hosts_t.sort()
    key = str(cls) + str(hosts_t) + str(excpt_classes)

    hosts = [item.split(':') for item in hosts]
    global thrift_clients
    if key not in thrift_clients:
        params = {
            'client_class':cls,
            'servers':['%s:%d' % (item[0], int(item[1])) for item in hosts],
            'options':{
                'protocol' : TBinaryProtocol.TBinaryProtocolAccelerated,
                #'protocol' : TBinaryProtocol.TBinaryProtocol,
                'retries' : retries,
                'timeout' : timeout,
                'connect_timeout': connect_timeout,
                # do not disconnect with server if exception of this type
                # it is application specialed.
                # raise it to caller.
                'exception_class_overrides': excpt_classes
            }
        }
        proxy = TracedRPCProxy(cls=ThriftClient, max_conn_num=max_conn_num, **params)
        thrift_clients[key] = proxy
    return thrift_clients[key]
