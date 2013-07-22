from __future__ import absolute_import

from zhwcore.client.memcache_r import get_mc_client

class TestCaseMemcacheClient(object):
    def __init__(self):
        self._hosts = ["127.0.0.1:11311", "127.0.0.1:11411", "127.0.0.1:11511"]

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_factory(self):
        c = get_mc_client(self._hosts)
        c2 = get_mc_client(self._hosts)
        from zhwcore.client import memcache_r
        assert len(memcache_r.mc_clients) == 1
        assert c == c2

        import random
        hosts = self._hosts
        random.shuffle(hosts)
        c3 = get_mc_client(hosts)
        assert len(memcache_r.mc_clients) == 1
        assert c2 == c3

        hosts = self._hosts
        hosts.append("127.0.0.1:11611")
        c4 = get_mc_client(hosts)
        assert len(memcache_r.mc_clients) == 2
        assert c3 != c4

    def test_get(self):
        c = get_mc_client(self._hosts)
        assert c.get('not_exist_key') == None

    def test_set(self):
        c = get_mc_client(self._hosts)
        k = 'test_case_key'
        v = 'v'
        c.delete(k)
        assert c.get(k) == None
        assert c.set(k, v) == 1
        assert c.get(k) == v
        c.delete(k)
