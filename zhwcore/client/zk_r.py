from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from threading import Lock

from zhwcore.common.singleton import Singleton


class ZookeeperClient(KazooClient):
    """
    zookeeper client that communicates with
    zookeeper cluster

    one instance is enough for one process
    so make it singleton here.

    """
    __metaclass__ = Singleton

    def __init__(self, *argv, **kwargs):
        super(ZookeeperClient, self).__init__(*argv, **kwargs)
        self._lock = Lock()
        self._started = False

    def start(self):
        """
        only start once

        """
        with self._lock:
            if self._started == True:
                return
            super(ZookeeperClient, self).start()
            self._started = True

    def stop(self):
        """
        only stop once

        """
        with self._lock:
            if self._started == False:
                return
            super(ZookeeperClient, self).stop()
            self._started = False

    def __getattr__(self, key):
        """
        make sure sequence call through lock

        """
        def _(*args, **kwargs):
            with self._lock:
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
    def __init__(self, zk_addr, service_addr, callback=None):
        """
        @zk_addr: is zookeeper cluster hosts
        @service_addr: is service address
            for example:
            /zhw/services/user/

        @callback: called when the children changed
        callback of the following form:

        def callback(hosts):
            pass

        """
        self._zk = ZookeeperClient(zk_addr)
        if service_addr[-1] != '/':
            raise Exception('service_addr must be end with "/", now:[%s]' % service_addr)
        self._service_addr = service_addr

        self._callback = callback

        #init connection to zookeeper
        self._zk.start()

        #watch children changed automatic
        self._watch_children()

    def get_hosts(self):
        """
        get hosts of the service address contains

        """
        nodes = self._get_children()
        hosts = self._get_nodes_value(nodes)
        return list(set(hosts))

    def _get_children(self):
        """
        get children of the service address

        """
        children = self._zk.get_children(self._service_addr)
        return children

    def _get_nodes_value(self, nodes):
        """
        get values stored in the nodes

        """
        hosts = []
        for node in nodes:
            host = self._get_value(self._service_addr + '/' + node)
            if host:
                hosts.append(host)
        return hosts

    def _get_value(self, path):
        """
        get value(host stored in the value) of the path

        """
        try:
            return self._zk.get(path)[0]
        except NoNodeError:
            return None

    def _watch_children(self):
        """
        watch the children changed event
        and call the callback

        """
        self._zk.ChildrenWatch(self._service_addr, self._children_changed)

    def _children_changed(self, children):
        """
        called when children changed

        """
        hosts = self._get_nodes_value(children)
        if self._callback:
            self._callback(list(set(hosts)))
