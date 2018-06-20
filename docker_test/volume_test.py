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
        response = self.v.create(base_test.volume_name, 'local')
        status_code = response.get('status_code')
        if status_code != 201:
            self.fail('Create volume FAIL : ' + str(status_code))
            
    def tearDown(self):
        response = self.v.remove(base_test.volume_name)
        status_code = response.get('status_code')
        if status_code != 204:
            self.fail('Remove volume FAIL : ' + str(status_code))
            
    def test_list(self):
        
        def check_list(v_list):
            status_code = v_list.get('status_code')
            if status_code == 200:
                volume_list = v_list.get('content').get('Volumes')
                self.assertEquals(len(volume_list), 1)
            else:
                self.fail('list: list volume fail, status_code : ' + str(status_code))
            if base_test.print_json:
                print 'list:' + json.dumps(v_list)
        check_list(self.v.list())
        check_list(self.v.list('test-volume'))

    def test_inspect(self):
        response = self.v.inspect(base_test.volume_name)
        status_code = response.get('status_code')
        if status_code == 200:
            volume_info = response.get('content')
            self.assertEqual(volume_info.get('Name'), base_test.volume_name)
            self.assertEqual(volume_info.get('Driver'), 'local')
            self.assertIsNotNone('Mountpoint')
        else:
            self.fail('inspect : get volume {0} fail, status_code : {1}'.format(base_test.volume_name, 
                                                                                str(status_code)))
        if base_test.print_json:
            print 'inspect:' + json.dumps(response)



            

