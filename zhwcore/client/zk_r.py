from kazoo.client import KazooClient
from threading import Lock

lock = Lock()

class ZookeeperClient(KazooClient):
    def __getattr__(self, key):
        with lock:
            def _(*args, **kwargs):
                func = getattr(self, key)
                return func(*args, **kwargs)
        return _

if __name__ == '__main__':
    #zk = KazooClient(hosts='127.0.0.1:2181')
    zk = ZookeeperClient(hosts='127.0.0.1:2181')
    zk.start()

    # Ensure a path, create if necessary
    zk.ensure_path("/my/favorite")

    # Create a node with data
    zk.create("/my/favorite/node", b"a value")
    
    @zk.ChildrenWatch("/my/favorite/node")
    def watch_children(children):
        print("Children are now: %s" % children)
    # Above function called immediately, and from then on
    
    @zk.DataWatch("/my/favorite")
    def watch_node(data, stat):
        print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    
    zk.stop()
