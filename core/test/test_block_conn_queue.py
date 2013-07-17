from common.block_conn_queue import BlockConnQueue

class T():
    pass

def test_block_conn_queue():
    q = BlockConnQueue(conn_class=T, max_conn_num=1, **{})
    assert isinstance(q.get(), T)
