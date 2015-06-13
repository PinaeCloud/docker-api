# coding=utf-8

class Image():
    def __init__(self, session):
        self.session = session
        
    def list(self, name = None, all = False, filters = None):
        params = {
            'filter': name,
            'all': 1 if all else 0,
            }
        url = self.session._url("/images/json")
        response = self.session._result(self.session._get(url, params = params), True)

        return response
    
