# coding=utf-8

import requests.adapters
import socket
import httplib

try:
    import requests.packages.urllib3 as urllib3
except ImportError:
    import urllib3

RecentlyUsedContainer = urllib3._collections.RecentlyUsedContainer

class UnixHTTPConnection(httplib.HTTPConnection, object):
    def __init__(self, base_url, unix_socket, timeout = 60):
        httplib.HTTPConnection.__init__(self, 'localhost', timeout=timeout)
        self.base_url = base_url
        self.unix_socket = unix_socket
        self.timeout = timeout

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.unix_socket)
        self.sock = sock


class UnixHTTPConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    def __init__(self, base_url, socket_path, timeout = 60):
        urllib3.connectionpool.HTTPConnectionPool.__init__(
            self, 'localhost', timeout=timeout
            )
        self.base_url = base_url
        self.socket_path = socket_path
        self.timeout = timeout

    def _new_conn(self):
        return UnixHTTPConnection(self.base_url, self.socket_path, self.timeout)


class UnixAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, socket_url, timeout = 60):
        socket_path = socket_url.replace('unix://', '')
        if not socket_path.startswith('/'):
            socket_path = '/' + socket_path
            
        self.socket_path = socket_path
        self.timeout = timeout
        self.pools = RecentlyUsedContainer(10, dispose_func=lambda p: p.close())
        super(UnixAdapter, self).__init__()

    def get_connection(self, url, proxies=None):
        with self.pools.lock:
            pool = self.pools.get(url)
            if pool:
                return pool

            pool = UnixHTTPConnectionPool(url, self.socket_path, self.timeout)
            self.pools[url] = pool

        return pool

    def close(self):
        self.pools.clear()
