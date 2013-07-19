def patch_gevent_dup():
    from socket import socket

    def timeout_dup(self):
        """dup() -> socket object

        Return a new socket object connected to the same system resource.
        Note, that the new socket does not inherit the timeout."""
        class _timeout_sock(object):
            def __init__(self, sock, timeout):
                self._sock = sock
                self.timeout = timeout
        #return socket(_sock=self._sock)
        return socket(_sock=_timeout_sock(sock=self._sock, timeout=self.timeout))

    socket.dup = timeout_dup
