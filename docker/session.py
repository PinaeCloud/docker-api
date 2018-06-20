# coding=utf-8

import os.path
import requests.adapters
import socket
import httplib

try:
    import requests.packages.urllib3 as urllib3
except ImportError:
    import urllib3

import json

from docker.utils import file_utils
from docker.utils import string_utils

RecentlyUsedContainer = urllib3._collections.RecentlyUsedContainer

def get_session(url):
    return Session(url)

class Session(requests.Session):
    def __init__(self, url = None):
        super(Session, self).__init__()
        
        if url is None:
            raise 'Docker URL is None'
        
        self.url = url
        
        self.timeout = 60
        
        if url.startswith('unix://'):
            unix_socket_adapter = UnixAdapter(url, 60)
            self.mount('http+unix://', unix_socket_adapter)
            self.url = 'http+unix://localhost'
        else:
            self.url = url
        
    def _set_request_timeout(self, kwargs):
        """Prepare the kwargs for an HTTP request by inserting the timeout
        parameter, if not already present."""
        kwargs.setdefault('timeout', self.timeout)
        return kwargs
    
    def _put(self, url, **kwargs):
        stream = kwargs.get('stream')
        if stream is not None and stream is True:
            return self.put(url, **kwargs)
        else:
            return self.put(url, **self._set_request_timeout(kwargs))

    def _post(self, url, **kwargs):
        stream = kwargs.get('stream')
        if stream is not None and stream is True:
            return self.post(url, **kwargs)
        else:
            return self.post(url, **self._set_request_timeout(kwargs))

    def _get(self, url, **kwargs):
        stream = kwargs.get('stream')
        if stream is not None and stream is True:
            return self.get(url, **kwargs)
        else:
            return self.get(url, **self._set_request_timeout(kwargs))
        
    def _post_json(self, url, data, **kwargs):
        req_data = {}
        if data is not None:
            for key in data:
                value = data[key]
                if value is not None:
                    req_data[key] = value
        
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Content-Type'] = 'application/json'
        return self.post(url, data=json.dumps(req_data), **kwargs)

    def _delete(self, url, **kwargs):
        return self.delete(url, **self._set_request_timeout(kwargs))

    def _url(self, path, versioned_api = True):
        url = '{0}{1}'.format(self.url, path)
        return url

    def _result(self, response, stream = False, with_headers = False):
        result = {}

        headers = response.headers
        content_type = headers.get('content-type')

        if stream:
            return self._stream_raw_result(response)
        else:
            if 'application/json' in content_type:
                result = self._to_json(response)
            elif 'application/vnd.docker.distribution.manifest' in content_type:
                result = self._to_json(response)
            elif 'application/octet-stream' in content_type or 'application/x-tar' in content_type:
                result = response
            elif 'application/vnd.docker.raw-stream' in content_type:
                result['content'] = response.content
            else:
                result['content'] = response.text
        
        if isinstance(result, dict):
            result['status_code'] = response.status_code
            result['content-type'] = content_type
            if with_headers:
                result['headers'] = headers
        
        return result
    
    def _to_json(self, response):
        result = {}
        try:
            result['content'] = response.json()
        except ValueError:
            result['content'] = response.text
        return result
    
    def _stream_raw_result(self, response, chunk_size = 1):
        for out in response.iter_content(chunk_size = chunk_size, decode_unicode = True):
            yield out
            
    def _stream_helper(self, response, decode = False):
        """Generator for data coming from a chunked-encoded HTTP response."""
        if response.raw._fp.chunked:
            reader = response.raw
            while not reader.closed:
                # this read call will block until we get a chunk
                data = reader.read(1)
                if not data:
                    break
                if reader._fp.chunk_left:
                    data += reader.read(reader._fp.chunk_left)
                if decode:
                    data = json.loads(data)
                yield data
        else:
            # Response isn't chunked, meaning we probably
            # encountered an error immediately
            yield self._result(response)
    
    def _read(self, path, tail=None):
        if string_utils.is_empty(path):
            raise ValueError('Path is Empty')
        if path.startswith('/'):
            filename = self.docker_path + path
        else:
            filename = os.path.join(self.docker_path, path)
        if os.path.exists(filename):
            result = file_utils.read_file(filename, tail)
            return result
        else:
            raise IOError('File {0} not found'.format(filename))
    
    def _get_docker_path(self):
        return self.docker_path
    
    def _get_url(self):
        return self.url
    
class UnixHTTPConnection(httplib.HTTPConnection, object):
    def __init__(self, url, unix_socket, timeout = 60):
        httplib.HTTPConnection.__init__(self, 'localhost', timeout=timeout)
        self.url = url
        self.unix_socket = unix_socket
        self.timeout = timeout

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.unix_socket)
        self.sock = sock


class UnixHTTPConnectionPool(urllib3.connectionpool.HTTPConnectionPool):
    def __init__(self, url, socket_path, timeout = 60):
        urllib3.connectionpool.HTTPConnectionPool.__init__(
            self, 'localhost', timeout=timeout
            )
        self.url = url
        self.socket_path = socket_path
        self.timeout = timeout

    def _new_conn(self):
        return UnixHTTPConnection(self.url, self.socket_path, self.timeout)


class UnixAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, socket_url, timeout = 60):
        socket_path = socket_url.replace('unix://', '')
        if not socket_path.startswith('/'):
            socket_path = '/' + socket_path
            
        self.socket_path = socket_path
        self.timeout = timeout
        self.pools = RecentlyUsedContainer(10, dispose_func = lambda p: p.close())
        super(UnixAdapter, self).__init__()

    def get_connection(self, url, proxies = None):
        with self.pools.lock:
            pool = self.pools.get(url)
            if pool:
                return pool

            pool = UnixHTTPConnectionPool(url, self.socket_path, self.timeout)
            self.pools[url] = pool

        return pool

    def close(self):
        self.pools.clear()
