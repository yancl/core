from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from threading import Lock


class ZookeeperClient(KazooClient):
    _lock = Lock()
    def __getattr__(self, key):
        def _(*args, **kwargs):
            with _lock:
                func = getattr(self, key)
                return func(*args, **kwargs)
        return _


class ServiceAddrResovler(object):
    """
    ServiceAddrResovler used to resovle all nodes hosts
    for example:
        /zhw/services/user/
                          ... bear000001
                          ... bear000002
                          ... tiger00001
                          ... tiger00002
        will return ['192.168.0.186:9090','192.168.0.186:9091',
                     '192.168.0.187:9090','192.168.0.187:9091']
        so that caller will connect them for later process

    """
    def __init__(self, zk_addr, service_addr):
        """
        zk_address is zookeeper cluster hosts
        service_addr is service address
            for example:
            /zhw/services/user/

        """
        self._zk = ZookeeperClient(zk_addr)
        self._service_addr = service_addr

    def get_hosts(self):
        """
        get hosts of the service address contains

        """
        hosts = []
        nodes = self._get_children()
        for node in nodes:
            host = self._get_value(self._service_addr + '/' + node)
            if host:
                hosts.append(host)
        return hosts

    def _get_children(self):
        """
        get children of the service address

        """
        children = self._zk.get_children(self._service_addr)
        return children

    def _get_value(self, path):
        """
        get value(host stored in the value) of the path

        """
        try:
            return self._zk.get(path)[0]
        except NoNodeError:
            return None
