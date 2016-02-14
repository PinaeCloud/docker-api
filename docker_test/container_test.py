# coding=utf-8

import unittest
import json
from docker import session
from docker import container
from docker import container_config
from twisted.trial.test.test_assertions import AssertTrueTests

class ContainerTest(unittest.TestCase):
    
    def setUp(self):
        s = session.get_session('unix://var/run/docker.sock')
        #s = session.get_session('http://192.168.228.130:2375')
        self.i = container.Container(s)
        
    def test_create(self):
        new_c = container_config.ContainerConfig()
        
        new_c.set_image('ubuntu:14.04')
        new_c.set_command('/bin/bash')
      
        new_c.add_label('Author', 'Huiyugeng')
        new_c.add_label('Version', 'v1.0')
        
        config = new_c.build_config()
        json_str = json.dumps(config)
        print json_str
        response = self.i.create(None, config)
        print response
        
    def test_list(self):
        container_list = self.i.list(None, True, True)
        print json.dumps(container_list)
        
    def test_get_config(self):
        container = self.i.get_config('12201463f0b3')
        print json.dumps(container)
        
    def test_get_status(self):
        container = self.i.get_status('12201463f0b3')
        print json.dumps(container)
        
    def test_rename(self):
        response = self.i.rename('e785120abd42', 'ubuntu-test-2')
        print json.dumps(response)
        
    def test_remove(self):
        response = self.i.remove('8ceb01806796')
        print response
        
    def test_top(self):
        response = self.i.top('12201463f0b3')
        print response
        
    def test_get_container_by_name(self):
        container = self.i.get_container_by_name('high_poincare')
        container_id = container.get('Id')
        self.assertTrue(container_id.startswith('12201463f0b3'))
        