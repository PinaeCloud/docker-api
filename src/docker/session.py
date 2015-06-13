# coding=utf-8

import json
import requests
import unix_conn

import version

def get_session(base_url):
    return Session(base_url)

class Session(requests.Session):
    def __init__(self, base_url=None):
        super(Session, self).__init__()

        self.base_url = base_url
        self.timeout = 60
        
        #setup docker daemon's url
        if base_url.startswith('unix://'):
            unix_socket_adapter = unix_conn.UnixAdapter(base_url, 60)
            self.mount('unix://', unix_socket_adapter)
            self.base_url = 'unix://localhost'
        else:
            self.base_url = base_url
            
        #try to connect docker daemon and get version
        try:
            response = version.get_version(self)
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
        return self.post(url, **self._set_request_timeout(kwargs))

    def _get(self, url, **kwargs):
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
        
        result['content-type'] = response.status_code
        
        
        if content_type == 'application/json':
            result['content'] = response.json()
        elif content_type == 'application/octet-stream' or content_type == 'application/x-tar':
            result['content'] = response.content
        else:
            result['content'] = response.text
            
        return result
    
    def _post_json(self, url, data, **kwargs):
        data2 = {}
        if data is not None:
            for key in data:
                value = data[key]
                if value is not None:
                    data2[key] = value

        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Content-Type'] = 'application/json'
        return self._post(url, data=json.dumps(data2), **kwargs)
