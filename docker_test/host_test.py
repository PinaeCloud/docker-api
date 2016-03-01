# coding=utf-8

import unittest
import json
from docker import session
from docker import host

from docker_test import base_test

class HostTest(unittest.TestCase):
    def setUp(self):
        self.c_session = session.get_session(base_test.session_url)
        self.h = host.Host(self.c_session)
        
    def test_info(self):
        response = self.h.info()
        status_code = response.get('status_code')
        if status_code == 200:
            content = response.get('content')
            self.assertEqual(content.get('OSType'), 'linux')
            self.assertEqual(content.get('CPUSet'), True)
            self.assertGreater(content.get('NCPU'), 0)
            self.assertGreater(content.get('MemTotal'), 0)
            self.assertGreater(content.get('Images'), 0)
        else:
            self.fail('info: get docker server info fail, status_code' + status_code)
        if base_test.print_json:
            print 'info:' + json.dumps(response)
    
    def test_version(self):
        response = self.h.version()
        status_code = response.get('status_code')
        if status_code == 200:
            content = response.get('content')
            self.assertEqual(content.get('Os'), 'linux')
            self.assertEqual(content.get('Arch'), 'amd64')
            self.assertIsNotNone(content.get('Version'))
            self.assertIsNotNone(content.get('ApiVersion'))
        else:
            self.fail('version: get docker server version fail, status_code' + status_code)
        if base_test.print_json:
            print 'version:' + json.dumps(response)
    
    def test_ping(self):
        response = self.h.ping()
        status_code = response.get('status_code')
        if status_code == 200:
            self.assertEqual(response.get('content'), 'OK')
        else:
            self.fail('ping: ping docker server fail, status_code' + status_code)
        if base_test.print_json:
            print 'ping:' + json.dumps(response)
            
    def test_auth_login(self):
        response = self.h.login('username', 'password', 'username@email.com', 'localhost')
        status_code = response.get('status_code')
        if status_code == 200:
            content = response.get('content')
            self.assertEqual(content.get('Status'), 'Login Succeeded')
        else:
            self.fail('long: long to docker registry fail, status_code' + status_code)
        if base_test.print_json:
            print 'login:' + json.dumps(response)
    
    def test_get_auth_config(self):
        response = self.h.get_auth_config('https://index.docker.io/v1/')
        self.assertIsNotNone(response.get('username'))
        self.assertIsNotNone(response.get('serveraddress'))
        if base_test.print_json:
            print 'get_auth_config:' + json.dumps(response)
    
    def test_get_all_auth_config(self):
        response = self.h.get_all_auth_config()
        self.assertGreater(len(response), 0)
        if base_test.print_json:
            print 'get_all_auth_config:' + json.dumps(response)

