# coding=utf-8

from version import check_version

class Container():
    def __init__(self, session):
        self.session = session
 
    @check_version
    def list(self, name = None, all = False, filters = None):
        params = {
            'filter': name,
            'all': 1 if all else 0,
            }
        url = self.session._url('/containers/json')
        response = self.session._result(self.session._get(url, params = params))
        return response
    
    @check_version
    def create(self, container_name, hostname, image, cmd):
        params = {
            'name': container_name,
            }
        config = {
            'Hostname': hostname,
            'Image': image,
            'Cmd' : cmd
            }
        url = self.session._url('/containers/create')
        response = self.session._result(self.session._post_json(url, data=config, params=params))
        return response
    
    @check_version
    def start(self, container_id):
        url = self.session._url('/containers/{0}/start'.format(container_id))
        response = self.session._result(self.session._post_json(url, data={}, params={}))
        return response
    
    @check_version
    def stop(self, container_id):
        url = self.session._url('/containers/{0}/stop'.format(container_id))
        response = self.session._result(self.session._post_json(url, data={}, params={}))
        return response
    
    @check_version
    def pause(self, container_id):
        url = self.session._url('/containers/{0}/pause'.format(container_id))
        response = self.session._result(self.session._post_json(url, data={}, params={}))
        return response