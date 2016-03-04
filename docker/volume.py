# coding=utf-8

from text import string_utils as str_utils

class Volume():
    
    def __init__(self, session):
        self.session = session
    
    def list(self, filters = None):
        params = {'filters': filters}
        url = self.session._url('/volumes')
        return self.session._result(self.session._get(url, params = params))
    
    def inspect(self, volume_name):
        url = self.session._url('/volumes/{0}'.format(volume_name))
        return self.session._result(self.session._get(url))
    
    def create(self, volume_name, driver = None, driver_opts = None):
        if str_utils.is_empty(volume_name):
            raise IOError('Volume name is Empty') 
        if driver_opts is not None and not isinstance(driver_opts, dict):
            raise TypeError('driver_opts must be a dictionary')

        req_data = {'Name': volume_name, 'Driver': driver, 'DriverOpts': driver_opts}
        url = self.session._url('/volumes/create')
        return self.session._result(self.session._post_json(url, data = req_data))
    
    def remove(self, volume_name):
        url = self.session._url('/volumes/{0}'.format(volume_name))
        return self.session._result(self.session._delete(url))
