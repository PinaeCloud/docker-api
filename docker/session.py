# coding=utf-8

import requests.adapters
import socket
import httplib

try:
    import requests.packages.urllib3 as urllib3
except ImportError:
    import urllib3

import json
import requests

from text import string_utils

import host

RecentlyUsedContainer = urllib3._collections.RecentlyUsedContainer


def get_session(base_url):
    return Session(base_url)

class Session(requests.Session):
    def __init__(self, base_url=None):
        super(Session, self).__init__()

        self.base_url = base_url
        self.timeout = 60
        
        #set docker server url
        if base_url.startswith('unix://'):
            unix_socket_adapter = UnixAdapter(base_url, 60)
            self.mount('unix://', unix_socket_adapter)
            self.base_url = 'unix://localhost'
        else:
            self.base_url = base_url
            
        #try to connect docker daemon and get version
        try:
            response = host.Host(self).get_version()
            if (response['status_code'] == 200):
                self.version = response['content']['ApiVersion']
            else:
                raise IOError('server {0} error'.format(base_url))
        except:
            raise IOError('connect to {0} fail'.format(base_url))
        
    def _set_request_timeout(self, kwargs):
        """Prepare the kwargs for an HTTP request by inserting the timeout
        parameter, if not already present."""
        kwargs.setdefault('timeout', self.timeout)
        return kwargs

    def _post(self, url, **kwargs):
        if 'params' in kwargs:
            url = self._build_params(url, kwargs.get('params'))
        return self.post(url, **self._set_request_timeout(kwargs))

    def _get(self, url, **kwargs):
        if 'params' in kwargs:
            url = self._build_params(url, kwargs.get('params'))
        return self.get(url, **self._set_request_timeout(kwargs))

    def _delete(self, url, **kwargs):
        return self.delete(url, **self._set_request_timeout(kwargs))

    def _url(self, path, versioned_api=True):
        url = '{0}{1}'.format(self.base_url, path)
        return url


    def _result(self, response):
        result = {}
        
        result['status_code'] = response.status_code
        
        headers = response.headers
        content_type = headers.get('content-type')
        
        result['content-type'] = content_type

        if content_type == 'application/json':
            result['content'] = response.json()
        elif content_type == 'application/octet-stream' or content_type == 'application/x-tar':
            result['content'] = response.content
        else:
            result['content'] = response.text
            
        return result
    
    def _post_json(self, url, data, **kwargs):
        req_data = {}
        if data is not None:
            for key in data:
                value = data[key]
                if value is not None:
                    req_data[key] = value
        
        if 'params' in kwargs:
            url = self._build_params(url, kwargs.get('params'))
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Content-Type'] = 'application/json'
        return self.post(url, data=json.dumps(req_data), **kwargs)
    
    def _build_params(self, url, params):
        param = ''
        for key in params:
            value = params.get(key)
            param = param + key + '=' + str(value)
            
        if string_utils.is_not_empty(param):
            url = url + '?' + param
        return url
    
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
