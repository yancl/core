from __future__ import absolute_import

from .block_conn_queue import BlockConnQueue

class RPCProxy(object):
    __slots__ = '_q'
    def __init__(self, cls, max_conn_num, **kwargs):
        self._q = BlockConnQueue(cls, max_conn_num, **kwargs)

    def __getattr__(self, key):
        def _(*args, **kwargs):
            try:
                conn = self._q.get()
                func = getattr(conn, key)
                return func(*args, **kwargs)
            finally:
                self._q.put(conn)
        return _

class TracedRPCProxy(RPCProxy):
    pass
