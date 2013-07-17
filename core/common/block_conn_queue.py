from Queue import Queue
MAX_CONN_NUM = 200

class BlockConnQueue(object):
    __slots__ = '_cls', '_kwargs', '_max_conn_num', '_q'
    def __init__(self, conn_class, max_conn_num, **kwargs):
        self._cls = conn_class 
        self._kwargs = kwargs
        self._max_conn_num = max_conn_num
        self._q = Queue(maxsize=max_conn_num)
        if self._max_conn_num > MAX_CONN_NUM:
            raise Exception('max conn num setting is too big(>%d),value:%d' % (MAX_CONN_NUM, self._max_conn_num))
        self._init_q()

    def get(self):
        return self._q.get(block=True)

    def put(self, conn):
        self._q.put(conn, block=False)

    def _init_q(self):
        for i in xrange(self._max_conn_num):
            self._q.put(self._cls(**self._kwargs))
