# coding=utf-8

import logging

from text import string_utils as str_utils
from docker.utils import auth

log = logging.getLogger(__name__)

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
        url = self.session._url('/images/search')
        response = self.session._result(self.session._get(url, params=params))
        return response
    
    def tag(self, image_name, repository, tag=None, force=False):
        params = {'tag': tag, 'repo': repository, 'force': 1 if force else 0 }
        url = self.session._url('/images/{0}/tag'.format(image_name))
        response = self.session._result(self.session._post(url, params = params))
        return response
    
    def create_by_file(self, filename, repository = None, tag = None):
        if str_utils.is_empty(filename):
            raise 'Filename is Empty'
        
        params = {'fromSrc' : '-', 'repo' : repository, 'tag' : tag}
        headers = {'Content-Type': 'application/tar'}
        
        url = self.session._url('/images/create')
        
        with open(filename, 'rb') as image_file:
            return self.session._result(
                self.session._post(url, data=image_file, params=params, headers=headers,
                           timeout=None))
        
    
    def create_by_url(self, url, repository = None, tag = None):
        if str_utils.is_empty(url):
            raise 'URL is Empty'
        
        params = {'fromSrc' : url, 'repo' : repository, 'tag' : tag}
        
        url = self.session._url('/images/create')
        response = self.session._result(self.session._post_json(url, data=None, params=params))
        return response
    
    def create_by_image(self, image_name, repository = None, tag = None):
        if str_utils.is_empty(image_name):
            raise 'Image name is Empty'
        
        params = {'fromImage' : image_name, 'repo' : repository, 'tag' : tag}
        
        url = self.session._url('/images/create')
        response = self.session._result(self.session._post_json(url, data=None, params=params))
        return response
    
    def remove(self, image_name, force = False, noprune = False):
        params = {'force': force, 'noprune': noprune}
        url = self.session._url('/images/{0}'.format(image_name))
        response = self.session._result(self.session._delete(url, params = params))
        return response
    
    def pull(self, repository, tag, auth_config = None):
        if str_utils.is_empty(repository):
            raise 'Repository name is Empty'
        if str_utils.is_empty(tag):
            raise 'Repository tag is Empty'
         
        registry, _ = auth.resolve_repository_name(repository)
        params = {'tag': tag, 'fromImage': repository}
        
        headers = {}
        self.__set_auth_to_header(headers, registry, auth_config)

        url = self.session._url('/images/create')
        response = self.session._post(url, params=params, headers=headers, timeout = None)

        return self.session._result(response)
    
    def push(self):
        pass
    
    def __set_auth_to_header(self, headers, registry, auth_config = None):
        
        if headers is None:
            headers = {}
        
        if auth_config is None:
            log.debug("loading from filesystem")
            self._auth_configs = auth.load_config()
            auth_config = auth.resolve_authconfig(self._auth_configs, registry)
        else:
            log.debug('Sending supplied auth config')
            
        if auth_config is not None:
            headers['X-Registry-Auth'] = auth.encode_header(auth_config)
        else:
            log.debug('No auth config found')
            

    

            
        
