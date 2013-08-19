from __future__ import absolute_import

from zhwcore.client.thrift_r import get_thrift_client

class TestCaseThriftClient(object):
    def __init__(self):
        self._hosts = ['127.0.0.1:10001']

    def test_factory(self):
        from user.gen.user.User import Client as UserClient
        c = get_thrift_client(UserClient, self._hosts)
        c2 = get_thrift_client(UserClient, self._hosts)
        from zhwcore.client import thrift_r
        assert len(thrift_r.thrift_clients) == 1
        assert c == c2

        import random
        hosts = self._hosts
        hosts.append('127.0.0.1:10002')
        random.shuffle(hosts)
        c3 = get_thrift_client(UserClient, hosts)
        assert len(thrift_r.thrift_clients) == 2
        assert c2 != c3


    def test_get_user(self):
        from user.gen.user.User import Client as UserClient
        c = get_thrift_client(UserClient, self._hosts)
        assert c.get_user(1) != None


class TestCaseThriftClientZK(object):
    def __init__(self):
        self._zk_addr = '127.0.0.1:2181'
        self._service_addr = '/zhw/services/user/'

    def test_factory(self):
        from user.gen.user.User import Client as UserClient
        c = get_thrift_client_zk(
            cls=UserClient,
            zk_addr=self._zk_addr,
            service_addr=self._service_addr
        )

        c2 = get_thrift_client_zk(
            cls=UserClient,
            zk_addr=self._zk_addr,
            service_addr=self._service_addr
        )
        from zhwcore.client import thrift_r
        assert len(thrift_r.thrift_clients) == 1
        assert c == c2

        import random
        hosts = self._hosts
        hosts.append('127.0.0.1:10002')
        random.shuffle(hosts)
        c3 = get_thrift_client_zk(
            cls=UserClient,
            zk_addr=self._zk_addr,
            service_addr=self._service_addr
        )
        assert len(thrift_r.thrift_clients) == 2
        assert c2 != c3


    def test_get_user(self):
        from user.gen.user.User import Client as UserClient
        c = get_thrift_client_zk(
            cls=UserClient,
            zk_addr=self._zk_addr,
            service_addr=self._service_addr
        )
        assert c.get_user(1) != None
