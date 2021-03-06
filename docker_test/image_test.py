# coding=utf-8

import unittest
import json

from docker import session
from docker import image

from docker_test import base_test

class ImageInfoTest(unittest.TestCase):
    
    def setUp(self):
        self.c_session = session.get_session(base_test.session_url)
        self.i = image.Image(self.c_session)
        
    def test_list(self):
        response = self.i.list()
        status_code = response.get('status_code')
        if status_code == 200:
            image_list = response.get('content')
            self.assertGreater(len(image_list), 0)
        else:
            self.fail('list: list images fail, status_code : ' + str(status_code))
        if base_test.print_json:
            print 'list:' + json.dumps(response)
            
        response = self.i.list('ubuntu:14.04')
        if status_code == 200:
            image_list = response.get('content')
            self.assertEquals(len(image_list), 1)
        else:
            self.fail('list: list images fail, status_code : ' + str(status_code))
        if base_test.print_json:
            print 'list ubuntu14.04:' + json.dumps(response)
            
        response = self.i.list('openssh')
        if status_code == 200:
            image_list = response.get('content')
            self.assertEquals(len(image_list), 1)
        else:
            self.fail('list: list images fail, status_code : ' + str(status_code))
        if base_test.print_json:
            print 'list openssh:' + json.dumps(response)

    def test_inspect(self):
        response = self.i.inspect(base_test.image_name, base_test.image_version)
        status_code = response.get('status_code')
        if status_code == 200:
            image_info = response.get('content')
            self.assertEqual(image_info.get('RepoTags')[0], '{0}:{1}'.format(base_test.image_name, 
                                                                                            base_test.image_version))
            self.assertGreater(image_info.get('VirtualSize'), 0)
            self.assertGreater(image_info.get('Size'), 0)
        else:
            self.fail('inspect : get image {0}:{1} fail, status_code : {2}'.format(base_test.image_name, 
                                                                                   base_test.image_version, 
                                                                                   str(status_code)))
        if base_test.print_json:
            print 'inspect:' + json.dumps(response)
            
    def test_history(self):
        response = self.i.history(base_test.image_name, base_test.image_version)
        status_code = response.get('status_code')
        if status_code == 200:
            image_history = response.get('content')
            self.assertEqual(len(image_history), 4)
        else:
            self.fail('history : get image {0}:{1} history fail, status_code : {2}'.format(base_test.image_name, 
                                                                                           base_test.image_version, 
                                                                                           str(status_code)))
        if base_test.print_json:
            print 'history:' + json.dumps(response)
            
    def test_search(self):
        response = self.i.search('interhui/mysql')
        status_code = response.get('status_code')
        if status_code == 200:
            image_list = response.get('content')
            self.assertEqual(len(image_list), 2)
        else:
            self.fail('search : search image {0} fail, status_code : {1}'.format('interhui/mysql', 
                                                                                 str(status_code)))
        if base_test.print_json:
            print 'search:' + json.dumps(response)
            
    def test_pull(self):
        self.i.remove('busybox:latest', True)
        stream = self.i.pull('busybox', 'latest', stream = True)
        
        if base_test.print_json:
            print '----------pulling busybox:latest-------------'
        for msg in stream:
            if msg is not None:
                if base_test.print_json:
                    print msg.strip()
        if base_test.print_json:
            print '--------pull busybox:latest finish-----------'
            
        resp_info = self.i.inspect('busybox', 'latest')
        self.assertEqual(resp_info.get('status_code'), 200)
        image_info = resp_info.get('content')
        self.assertEqual(image_info.get('RepoTags')[0], '{0}:{1}'.format('busybox', 'latest'))
        
        