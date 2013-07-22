from __future__ import absolute_import

from zhwcore.client.thrift_r import get_thrift_client

class TestCaseThriftClient(object):
    def __init__(self):
        self._hosts = [('127.0.0.1', 9523)]
        self._protocol_path = '/home/yancl/env/web/kantuban'

    def setup(self):
        import sys
        sys.path.insert(0, self._protocol_path)

    def teardown(self):
        import sys
        del sys.path[0]

    def test_factory(self):
        from protocol.genpy.tservices import TServices
        c = get_thrift_client(TServices.Client, self._hosts)
        c2 = get_thrift_client(TServices.Client, self._hosts)
        from zhwcore.client import thrift_r
        assert len(thrift_r.thrift_clients) == 1
        assert c == c2

        import random
        hosts = self._hosts
        hosts.append(('127.0.0.1', 9524))
        random.shuffle(hosts)
        c3 = get_thrift_client(TServices.Client, hosts)
        assert len(thrift_r.thrift_clients) == 2
        assert c2 != c3


    def test_get_user(self):
        from protocol.genpy.tservices import TServices
        c = get_thrift_client(TServices.Client, self._hosts)
        assert c.get_user(1) != None
