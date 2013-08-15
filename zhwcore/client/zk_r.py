from kazoo.client import KazooClient
from threading import Lock


class ZookeeperClient(KazooClient):
    _lock = Lock()
    def __getattr__(self, key):
        def _(*args, **kwargs):
            with _lock:
                func = getattr(self, key)
                return func(*args, **kwargs)
        return _
