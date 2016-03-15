# coding=utf-8

import unittest
import json
from docker import session
from docker import network

from docker_test import base_test

class NetworkTest(unittest.TestCase):
    
    def setUp(self):
        self.c_session = session.get_session(base_test.session_url)
        self.n = network.Network(self.c_session)
        response = self.n.create(base_test.network_name, 'bridge')
        status_code = response.get('status_code')
        if status_code != 201:
            self.fail('Create network FAIL : ' + str(status_code))
            
    def tearDown(self):
        response = self.n.remove(base_test.network_name)
        status_code = response.get('status_code')
        if status_code != 200:
            self.fail('Remove network FAIL : ' + str(status_code))
            
    def test_list(self):
        response = self.n.list()
        status_code = response.get('status_code')
        if status_code == 200:
            volume_list = response.get('content')
            self.assertGreater(len(volume_list), 0)
        else:
            self.fail('list: list network fail, status_code : ' + str(status_code))
        if base_test.print_json:
            print 'list:' + json.dumps(response)
    
    def test_inspect(self):
        response = self.n.inspect(base_test.network_name)
        status_code = response.get('status_code')
        if status_code == 200:
            volume_info = response.get('content')
            self.assertEqual(volume_info.get('Name'), base_test.network_name)
            self.assertEqual(volume_info.get('Driver'), 'bridge')
        else:
            self.fail('inspect : get network {0} fail, status_code : {1}'.format(base_test.network_name, 
                                                                                str(status_code)))
        if base_test.print_json:
            print 'inspect:' + json.dumps(response)

        
        