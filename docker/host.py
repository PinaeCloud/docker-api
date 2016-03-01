# coding=utf-8

import os

from docker.utils import auth

class Host():
    def __init__(self, session):
        self._auth_configs = None
        self.session = session
        
    def info(self):
        url = self.session._url('/info')
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def version(self):
        url = self.session._url('/version')
        response = self.session._result(self.session._get(url))
        return response
    
    def ping(self):
        url = self.session._url('/_ping')
        return self.session._result(self.session._get(url))
    
    def login(self, username, password = None, email = None, registry = None):
        
        registry = registry or auth.INDEX_URL
        req_data = {'username': username, 'password': password, 'email': email, 'serveraddress': registry}
        
        url = self.session._url('/auth')
        
        response = self.session._post_json(url, data = req_data)
        if response.status_code == 200:
            if self._auth_configs is None:
                self._auth_configs = {}
            self._auth_configs[registry] = req_data
            
        return self.session._result(response)
    
    def get_auth_config(self, registry, username = None):
        if registry is None:
            return None
        
        if self._auth_configs is None:
            self._load_auth_config()
            
        authcfg = auth.resolve_authconfig(self._auth_configs, registry)
        # If we found an existing auth config for this registry and username
        # combination, we can return it immediately unless reauth is requested.
        if authcfg:
            if username and authcfg.get('username', None) != username:
                return None
            
        return authcfg
    
    def get_all_auth_config(self):
        if self._auth_configs is None:
            self._load_auth_config()
        return self._auth_configs
    
    def _load_auth_config(self, cfg_file = None):
        if cfg_file is not None and os.path.exists(cfg_file):
            self._auth_configs = auth.load_config(cfg_file)
        elif not self._auth_configs:
            self._auth_configs = auth.load_config()
            