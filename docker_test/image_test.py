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
        image_list = self.i.list()
        print 'list:' + json.dumps(image_list)
        
    def test_inspect(self):
        image_info = self.i.inspect(base_test.image_name, base_test.image_version)
        print 'inspect:' + json.dumps(image_info)