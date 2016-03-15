# coding=utf-8

from docker.utils import decorators

from text import string_utils as str_utils

class Network():
    
    def __init__(self, session):
        self.session = session
    
    def list(self, filters = None):
        params = {'filters': filters}
        url = self.session._url('/networks')
        return self.session._result(self.session._get(url, params = params))
    
    def inspect(self, network_name):
        url = self.session._url('/networks/{0}'.format(network_name))
        return self.session._result(self.session._get(url))
    
    def create(self, network_name, driver = None, ipam = None, options = None, internal = True):
        if str_utils.is_empty(network_name):
            raise IOError('Network name is Empty') 
        if ipam is not None and not isinstance(ipam, dict):
            raise TypeError('driver_opts must be a dictionary')

        req_data = {'Name': network_name, 'Driver': driver, 
                    'IPAM': ipam, 'Options': options,
                    'Internal': internal
                    }
        url = self.session._url('/networks/create')
        return self.session._result(self.session._post_json(url, data = req_data))
    
    def remove(self, network_name):
        url = self.session._url('/networks/{0}'.format(network_name))
        return self.session._result(self.session._delete(url))
    
    @decorators.check_container
    def connect(self, network_name, container_id, ipv4 = None, ipv6 = None):
        if str_utils.is_empty(network_name):
            raise ValueError('Network name is Empty')
        ipam = {}
        if not ipv4:
            ipam['IPv4Address'] = ipv4
        if not ipv6:
            ipam['IPv6Address'] = ipv6
        req_data = {
                    'Container' : container_id,
                    'EndpointConfig' : {'IPAMConfig' : ipam}
                          }
        url = self.session._url('/networks/{0}/connect'.format(network_name))
        return self.session._result(self.session._post_json(url, data = req_data))
    
    @decorators.check_container
    def disconnect(self, network_name, container_id, force = False):
        if str_utils.is_empty(network_name):
            raise ValueError('Network name is Empty')
        req_data = {
                    'Container' : container_id,
                    'Force' : force
                          }
        url = self.session._url('/networks/{0}/disconnect'.format(network_name))
        return self.session._result(self.session._post_json(url, data = req_data))
    