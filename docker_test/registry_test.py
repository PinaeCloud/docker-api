# coding=utf-8

import unittest
import json

from docker import session
from docker import registry

from docker_test import base_test

class RegistryTest(unittest.TestCase):
    
    def setUp(self):
        self.c_session = session.get_session(base_test.registry_url)
        self.r = registry.Registry(self.c_session)
    
    def test_list(self):
        response = self.r.list(True)
        if base_test.print_json:
            print 'list:' + json.dumps(response)
    
    def test_inspect(self):
        response = self.r.inspect('mysql-5.6', 'latest')
        if base_test.print_json:
            print 'inspect:' + json.dumps(response)