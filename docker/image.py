# coding=utf-8

class Image():
    def __init__(self, session):
        self.session = session
        
    def list(self, name = None, show_all = False, filters = None):
        params = {}
        if name != None:
            params['filter'] = name
        if all == True:
            params['all'] = 1

        url = self.session._url("/images/json")
        response = self.session._result(self.session._get(url, params = params), True)

        return response
    
    def pull(self):
        pass
    
    def push(self):
        pass
    
