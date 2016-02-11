# coding=utf-8

class Container():
    def __init__(self, session):
        self.session = session
 
    def list(self, name = None, all = False, filters = None):
        params = {
            'filter': name,
            'all': 1 if all else 0,
            }
        url = self.session._url('/containers/json')
        response = self.session._result(self.session._get(url, params = params))
        return response
    
    def create(self, name, image, container_config):
        #check container name
        params = {
            'name': name,
            }

        url = self.session._url('/containers/create')
        response = self.session._result(self.session._post_json(url, data=container_config, params=params))
        return response
    
    def rename(self, container_id, new_name):
        if new_name:
            params = {'name' : new_name}
        
        #判断容器是否重名
        
        url = self.session._url('/containers/{0}/rename'.format(container_id))
        response = self.session._result(self.session._post(url, params))
        return response

    def remove(self, container_id, volumes=False, force=False):
        
        params = {
            'v' : volumes,
            'force' : force 
            }
        
        url = self.session._url('/containers/{0}/json'.format(container_id))
        response = self.session._result(self.session._delete(url, params))
        return response
    
    def get_config(self, container_id):
        url = self.session._url('/containers/{0}/json'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def get_status(self, container_id):
        url = self.session._url('/containers/{0}/stats'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response

    def top(self, container_id):
        url = self.session._url('/containers/{0}/top'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def start(self, container_id):
        url = self.session._url('/containers/{0}/start'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def stop(self, container_id, wait=None):
        if wait:
            params = {'t' : wait}
            
        url = self.session._url('/containers/{0}/stop'.format(container_id))
        response = self.session._result(self.session._post(url, params))
        return response

    def restart(self, container_id, wait=None):
        if wait:
            params = {'t' : wait}
            
        url = self.session._url('/containers/{0}/stop'.format(container_id))
        response = self.session._result(self.session._post(url, params))
        return response
    
    def kill(self, container_id, signal=None):
        if signal:
            params = {'signal' : signal}
            
        url = self.session._url('/containers/{0}/kill'.format(container_id))
        response = self.session._result(self.session._post(url, params))
        return response
    
    def pause(self, container_id):
        url = self.session._url('/containers/{0}/pause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def unpause(self, container_id):
        url = self.session._url('/containers/{0}/unpause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    