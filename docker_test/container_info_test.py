# coding=utf-8

import unittest
import json
from docker import session
from docker import container
from docker import container_config

class ContainerInfoTest(unittest.TestCase):
    
    def setUp(self):
        self.c_session = session.get_session('http://192.168.228.130:2375')
        self.c_name = 'test-container'
        self.i = container.Container(self.c_session)
        c_cfg = container_config.ContainerConfig()
        c_cfg.set_image('busybox:latest')
        c_cfg.set_command('/bin/sh')
        self.i.create(self.c_name, c_cfg)
        self.i.start(self.c_name)
      
    def test_list(self):
        container_list = self.i.list(True, True)
        print 'list:' + json.dumps(container_list)
        
    def test_get_config(self):
        container = self.i.get_config(self.c_name)
        print 'get_config:' + json.dumps(container)
        
    def test_get_status(self):
        container = self.i.get_status(self.c_name)
        print 'get_status:' + json.dumps(container)
        
    def test_top(self):
        tops = self.i.top(self.c_name)
        print 'top:' + json.dumps(tops)
   
    def test_get_container_by_name(self):
        container = self.i.get_container_by_name(self.c_name)
        print 'get_container_by_name:' + json.dumps(container)
        
    def teardown(self):
        self.i.stop(self.c_name)
        self.i.remove(self.c_name, volumes = True, force = True)
        
class ContainerLogTest(unittest.TestCase):
    
    def setUp(self):
        self.c_session = session.get_session('http://192.168.228.130:2375')
        self.i = container.Container(self.c_session)
        self.c_name = '91379f39ec12'
    '''    
    def test_logs(self):
        logs = self.i.logs(self.c_name)
        print 'logs:' + json.dumps(logs)
        
    def test_logs_with_stream(self):
        for log in self.i.logs_stream(self.c_name):
            print log
    '''
    def test_log_local(self):
        self.i.logs_local(self.c_name)
            