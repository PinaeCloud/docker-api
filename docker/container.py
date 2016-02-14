# coding=utf-8

import types

from text import string_utils as str_utils

class Container():
    def __init__(self, session):
        self.session = session
 
    def list(self, show_all=False, show_size=False, status=None, labels=None, exit_code=None):
        params = {}
        params['all'] = True if show_all == True else False
        params['size'] = True if show_size == True else False
        
        filters = {}
        if status != None:
            filters['status'] = status
        if labels != None and len(labels) > 0 and type(labels) == types.DictionaryType:
            filters['label'] = labels
        if exit_code != None:
            filters['exit_code'] = exit_code
        if len(filters) > 0:
            params['filters'] = filters
            
        url = self.session._url('/containers/json')
        response = self.session._result(self.session._get(url, params=params))
     
        return response
    
    def get_container_by_name(self, name):
        response = self.list(None, True)
        if response != None and response.get('status_code') == 200:
            container_list = response.get('content')
            if container_list != None:
                for container in container_list:
                    if 'Names' in container:
                        container_names = container.get('Names')
                        for container_name in container_names:
                            if name in container_name:
                                return container
        return None
    
    def get_config(self, container_id):
        url = self.session._url('/containers/{0}/json'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def get_status(self, container_id):
        url = self.session._url('/containers/{0}/stats'.format(container_id))
        response = self.session._result(self.session._get(url, params={'stream': False}))
        return response

    def top(self, container_id):
        url = self.session._url('/containers/{0}/top'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def create(self, name, container_cfg):
        # check container name
        params = {}
        if str_utils.is_not_empty(name):
            params['name'] = name

        url = self.session._url('/containers/create')
        response = self.session._result(self.session._post_json(url, data=container_cfg, params=params))
        return response
    
    def rename(self, container_id, new_name):
        if new_name:
            params = {'name' : new_name}
        
        url = self.session._url('/containers/{0}/rename'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response

    def remove(self, container_id, volumes=False, force=False):
        params = {}
        params['v'] = True if volumes == True else False
        params['force'] = True if force == True else False
        
        url = self.session._url('/containers/{0}'.format(container_id))
        response = self.session._result(self.session._delete(url, params=params))
        return response
    
    def start(self, container_id):
        url = self.session._url('/containers/{0}/start'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def stop(self, container_id, wait=None):
        params = {}
        if wait:
            params['t'] = wait
            
        url = self.session._url('/containers/{0}/stop'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response

    def restart(self, container_id, wait=None):
        params = {}
        if wait:
            params['t'] = wait
            
        url = self.session._url('/containers/{0}/restart'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response
    
    def kill(self, container_id, signal=None):
        params = {}
        if signal:
            params['signal'] = signal
            
        url = self.session._url('/containers/{0}/kill'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response
    
    def pause(self, container_id):
        url = self.session._url('/containers/{0}/pause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def unpause(self, container_id):
        url = self.session._url('/containers/{0}/unpause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
