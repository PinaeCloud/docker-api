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
        response = self.session._result(self.session._get(url, params = params))

        return response
    
    def inspect(self, image_name, version = None):
        if version != None:
            image_name = image_name + ':' + version
        url = self.session._url('/images/{0}/json'.format(image_name))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def history(self, image_name):
        url = self.session._url('/images/{0}/history'.format(image_name))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def pull(self):
        pass
    
    def push(self):
        pass
    
