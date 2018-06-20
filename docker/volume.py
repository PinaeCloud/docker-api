# coding=utf-8

from docker.utils import string_utils

class Volume():
    
    def __init__(self, session):
        self.session = session
    
    def list(self, volume_name = None, filters = None):
        params = {}
        if filters:
            params['filters'] = filters
        url = self.session._url('/volumes')
        response = self.session._result(self.session._get(url, params = params))
        if response.get('status_code') == 200 and volume_name:
            volume_list = []
            content = response.get('content').get('Volumes')
            for volume in content:
                _vol_name = volume.get('Name')
                if volume_name in _vol_name:
                    volume_list.append(volume)
            response['content']['Volumes'] = volume_list
        return response
                
    
    def inspect(self, volume_name):
        url = self.session._url('/volumes/{0}'.format(volume_name))
        return self.session._result(self.session._get(url))
    
    def create(self, volume_name, driver = None, driver_opts = None):
        if string_utils.is_empty(volume_name):
            raise IOError('Volume name is Empty') 
        if driver_opts is not None and not isinstance(driver_opts, dict):
            raise TypeError('driver_opts must be a dictionary')

        req_data = {'Name': volume_name, 'Driver': driver, 'DriverOpts': driver_opts}
        url = self.session._url('/volumes/create')
        return self.session._result(self.session._post_json(url, data = req_data))
    
    def remove(self, volume_name):
        url = self.session._url('/volumes/{0}'.format(volume_name))
        return self.session._result(self.session._delete(url))
    
    def remove_unused(self):
        url = self.session._url('/volumes/prune')
        return self.session._result(self.session._post_json(url, params={}))
