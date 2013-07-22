from __future__ import absolute_import

from zhwcore.client.redis_r import get_redis_client

class TestCaseRedisClient(object):
    def __init__(self):
        self._conf = 'test/conf/redis.conf'
        self._conf2 = 'test/conf/redis2.conf'

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_factory(self):
        c = get_redis_client(self._conf)
        c2 = get_redis_client(self._conf)
        from zhwcore.client import redis_r
        assert c == c2
        assert len(redis_r.rs_clients) == 1

        c3 = get_redis_client(self._conf2)
        assert c2 != c3
        assert len(redis_r.rs_clients) == 2

    def test_get(self):
        k = 'not_exist_key'
        c = get_redis_client(self._conf)
        assert c.get_conn(k).get(k) == None

    def test_set(self):
        k = 'test_case_redis_key'
        v = 'v'
        c = get_redis_client(self._conf)
        c.get_conn(k).delete(k)
        assert c.get_conn(k).get(k) == None
        assert c.get_conn(k).set(k, v) == 1
        assert c.get_conn(k).get(k) == v
        c.get_conn(k).delete(k)
