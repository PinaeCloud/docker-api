# coding=utf-8

import logging

logger = logging.getLogger(__name__)

class Registry():
    def __init__(self, session):
        self.session = session
        
    def list(self, detail = False, size = None):
        
        params = {}
        if size:
            params['n'] = size
        
        url = self.session._url('/v2/_catalog')
        response = self.session._result(self.session._get(url, params = params))
        
        if response.get('status_code') == 200:
            if detail:
                img_detail_list = []
                content = response.get('content')
                if content and content.get('repositories'):
                    img_list = content.get('repositories')
                    for img_name in img_list:
                        img_tag_url = self.session._url('/v2/{0}/tags/list'.format(img_name))
                        
                        img_tag_resp = self.session._result(self.session._get(img_tag_url))
                        if img_tag_resp.get('status_code') == 200:
                            img_detail_list.append(img_tag_resp.get('content'))
                        
                response['content'] = img_detail_list
                
        return response
    
    def inspect(self, image, tag):
        if not image or not tag:
            raise ValueError('Image name or image tag is Empty')
        url = self.session._url('/v2/{0}/manifests/{1}'.format(image, tag))
        response = self.session._result(self.session._get(url), with_headers = True)
        if response.get('status_code') == 200:
            content = response.get('content')
            if isinstance(content, dict):
                headers = response.get('headers')
                content_digest = headers.get('Docker-Content-Digest')
                content['digest'] = content_digest
                
                response['content'] = content
                del response['headers']
        
        return response
        