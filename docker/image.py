# coding=utf-8

from text import string_utils as str_utils

class Image():
    def __init__(self, session):
        self.session = session
        
    def list(self, show_all = False, filters = None):
        params = {}
        params['all'] = 1 if all == True else 0

        url = self.session._url("/images/json")
        response = self.session._result(self.session._get(url, params = params))

        return response
    
    def inspect(self, image_name, version = None):
        if str_utils.is_empty(image_name):
            raise 'Image name is Empty'
        if version != None:
            image_name = image_name + ':' + version
        url = self.session._url('/images/{0}/json'.format(image_name))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def history(self, image_name, version = None):
        if str_utils.is_empty(image_name):
            raise 'Image name is Empty'
        if version != None:
            image_name = image_name + ':' + version
        url = self.session._url('/images/{0}/history'.format(image_name))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def search(self, image_name):
        if str_utils.is_empty(image_name):
            raise 'Image name is Empty'
        params = {}
        params['term'] = image_name
        url = self.session._url('/images/search'.format(image_name))
        response = self.session._result(self.session._get(url, params=params))
        return response
    
    def build(self, docker_file):
        pass
    
    def tag(self):
        pass
    
    def import_image(self):
        pass
    
    def export_image(self):
        pass
    
    def pull(self):
        pass
    
    def push(self):
        pass
    
    def create(self):
        pass
    
    def remove(self):
        pass
    

            
        
