# coding=utf-8

import unittest
import json
from docker import session
from docker import container

from docker_test import base_test

class ContainerInfoTest(unittest.TestCase):
    
    def setUp(self):
        self.c_name = base_test.container_name
        
        self.c_session = session.get_session(base_test.session_url)
        self.c = container.Container(self.c_session)
        c_cfg = base_test.get_container()
        self.i.create(self.c_name, c_cfg)
        self.i.start(self.c_name)
      
    def test_list(self):
        container_list = self.c.list(True, True)
        print 'list:' + json.dumps(container_list)
        
    def test_inspect(self):
        container = self.c.inspect(self.c_name)
        print 'inspect:' + json.dumps(container)
        
    def test_status(self):
        container = self.c.status(self.c_name)
        print 'status:' + json.dumps(container)
        
    def test_top(self):
        tops = self.c.top(self.c_name)
        print 'top:' + json.dumps(tops)
        
    def teardown(self):
        self.c.stop(self.c_name)
        self.c.remove(self.c_name, volumes = True, force = True)
        
class ContainerLogTest(unittest.TestCase):
    
    def setUp(self):
        self.c_name = base_test.container_name
        
        self.c_session = session.get_session(base_test.session_url)
        self.c = container.Container(self.c_session)
        
    '''    
    def test_logs(self):
        logs = self.c.logs(self.c_name)
        print 'logs:' + json.dumps(logs)
        
    def test_logs_with_stream(self):
        for log in self.c.logs_stream(self.c_name):
            print log
    '''
    def test_log_local(self):
        self.c.logs_local(self.c_name)
            