from __future__ import absolute_import

from zhwcore.client.zk_r import ServiceAddrResovler

class TestCaseServiceAddrResovler(object):
    def __init__(self, zk_addr='127.0.0.1:2181', service_addr='/zhw/services/user/'):
        self._resovler = ServiceAddrResovler(zk_addr=zk_addr, service_addr=service_addr)

    def test_get_hosts(self):
        assert self._resovler.get_hosts() == ['192.168.0.186:10001']
