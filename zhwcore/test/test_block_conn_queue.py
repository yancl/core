from nose.tools import *
from Queue import Empty

from zhwcore.common.block_conn_queue import BlockConnQueue

class T():
    pass

class TestCaseBlockQueue(object):
    def test_block_conn_queue_container_type(self):
        q = BlockConnQueue(conn_class=T, max_conn_num=1, **{})
        c = q.get()
        assert isinstance(c, T)
    
    def test_block_conn_queue_get_put(self):
        q = BlockConnQueue(conn_class=T, max_conn_num=1, **{})
        c = q.get()
        assert isinstance(c, T)
        q.put(c)
        assert isinstance(q.get(), T)
    
    @raises(Empty)
    def test_block_conn_queue_empty_timeout(self):
        q = BlockConnQueue(conn_class=T, max_conn_num=1, **{})
        assert isinstance(q.get(), T)
        q.get(timeout=1)
