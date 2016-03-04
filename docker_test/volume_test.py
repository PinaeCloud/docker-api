# coding=utf-8

import unittest
import json
from docker import session
from docker import volume

from docker_test import base_test

class VolumeTest(unittest.TestCase):
    def setUp(self):
        self.c_session = session.get_session(base_test.session_url)
        self.v = volume.Volume(self.c_session)
        
    def test_list(self):
        response = self.v.list()
        status_code = response.get('status_code')
        if status_code == 200:
            volume_list = response.get('content')
            self.assertGreater(len(volume_list), 0)
        else:
            self.fail('list: list volume fail, status_code : ' + str(status_code))
        if base_test.print_json:
            print 'list:' + json.dumps(response)
    
    def test_inspect(self):
        response = self.v.inspect('mysql_data')
        status_code = response.get('status_code')
        if status_code == 200:
            volume_info = response.get('content')
            self.assertEqual(volume_info.get('Driver'), 'local')
            self.assertIsNotNone('Mountpoint')
        else:
            self.fail('inspect : get volume mysql_data fail, status_code : {0}'.format(str(status_code)))
        if base_test.print_json:
            print 'inspect:' + json.dumps(response)
    
    def test_create(self):
        self.v.remove('temp_data')
        response = self.v.create('temp_data', 'local')
        status_code = response.get('status_code')
        if status_code == 201:
            resp_info = self.v.inspect('temp_data')
            self.assertEqual(resp_info.get('status_code'), 200)
            self.assertEqual(resp_info.get('content').get('Name'), 'temp_data')
            self.assertEqual(resp_info.get('content').get('Driver'), 'local')

            

