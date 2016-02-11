# coding=utf-8

class Host():
    def __init__(self, session):
        self.session = session
        
    def get_info(self):
        url = self.session._url('/info')
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def get_version(self):
        url = self.session._url('/version')
        response = self.session._result(self.session._get(url))
        return response