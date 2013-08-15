from kazoo.client import KazooClient
from threading import Lock


class ZookeeperClient(KazooClient):
    _lock = Lock()
    def __getattr__(self, key):
        with _lock:
            def _(*args, **kwargs):
                func = getattr(self, key)
                return func(*args, **kwargs)
        return _
