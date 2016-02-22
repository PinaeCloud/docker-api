# coding=utf-8

import time
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
        c_cfg = self.c.status(self.c_name)
        if c_cfg.get('status_code') != 200:
            c_cfg = base_test.get_container()
            result = self.c.create(self.c_name, c_cfg)
            if result.get('status_code') == 201:
                result = self.c.start(self.c_name)
                if result.get('status_code') != 204:
                    print 'Stop container FAIL : ' + result.get('status_code')
            else:
                print 'Create container FAIL : ' + result.get('status_code')
        
      
    def test_list(self):
        c_list = self.c.list(True, True)
        status_code = c_list.get('status_code')
        if status_code == 200:
            self.assertEqual(len(c_list.get('content')), 1)
            c_cfg = c_list.get('content')[0]
            self.assertIsNotNone(c_cfg.get('Id'))
            self.assertEqual(c_cfg.get('Status').startswith('Up'))
            self.assertTrue(c_cfg.get('Image'), 'interhui/openssh:latest')
        else:
            self.fail('list : not any container, status_code :' + status_code)
            
        if base_test.print_json:
            print 'list : ' + json.dumps(c_list)
        
    def test_inspect(self):
        c_inspect = self.c.inspect(self.c_name)
        status_code = c_inspect.get('status_code')
        if status_code == 200:
            content = c_inspect.get('content')
            self.assertEqual(content.get('State').get('Running'), True)
            self.assertTrue(content.get('State').get('Pid') > 0)
            self.assertTrue(content.get('Config').get('Image'), 'interhui/openssh:latest')
        else:
            self.fail('inspect : not container {0}, status_code : {1}'.format(self.c_name, status_code))
            
        if base_test.print_json:
            print 'list : ' + json.dumps(c_inspect)
        
    def test_status(self):
        c_status = self.c.status(self.c_name)
        status_code = c_status.get('status_code')
        if status_code == 200:
            content = c_status.get('content')
            self.assertIsNotNone(content.get('read'))
            self.assertTrue(content.get('memory_stats').get('usage') > 0)
            self.assertTrue(content.get('cpu_stats').get('cpu_usage').get('total_usage') > 0)
        else:
            self.fail('status : not container {0} or {0} not running, status_code : {1}'.format(self.c_name, status_code))
        if base_test.print_json:
            print 'status:' + json.dumps(container)
        
    def test_top(self):
        c_tops = self.c.top(self.c_name)
        status_code = c_tops.get('status_code')
        if status_code == 200:
            processes = c_tops.get('content').get('Processes')
            self.assertEqual(len(processes), 1)
            self.assertEqual(processes[0], 'root')
            self.assertEqual(processes[7], '/usr/sbin/sshd -D')
        else:
            self.fail('top : not container {0} or {0} not running, status_code : {1}'.format(self.c_name, status_code))
        if base_test.print_json:
            print 'top:' + json.dumps(c_tops)
        
    def tearDown(self):
        result = self.c.stop(self.c_name)
        if result.get('status_code') == 204:
            result = self.c.remove(self.c_name, volumes = True, force = True)
            if result.get('status_code') != 204:
                print 'Remove container FAIL : ' + result.get('status_code')
        else:
            print 'Stop container FAIL : ' + result.get('status_code')


class ContainerLogTest(unittest.TestCase):
    
    
    def setUp(self):
        self.c_name = base_test.container_name
       
        self.c_session = session.get_session(base_test.session_url)
        self.c = container.Container(self.c_session)
    
        c_cfg = self.c.status(self.c_name)
        if c_cfg.get('status_code') != 200:
            c_cfg = base_test.get_container_with_log()
            result = self.c.create(self.c_name, c_cfg)
            if result.get('status_code') == 201:
                result = self.c.start(self.c_name)
                if result.get('status_code') != 204:
                    print 'Stop container FAIL : ' + result.get('status_code')
            else:
                print 'Create container FAIL : ' + result.get('status_code')
    
    def test_logs(self):
        time.sleep(10)
        logs = self.c.logs(self.c_name)
        print 'logs:' + json.dumps(logs)

    def test_logs_with_stream(self):
        for log in self.c.logs_stream(self.c_name):
            print log
    
    def test_logs_local(self):
        print len(self.c.logs_local(self.c_name, True, True, '2016-02-22 00:00:00'))

    
    def tearDown(self):
        result = self.c.stop(self.c_name)
        if result.get('status_code') == 204:
            result = self.c.remove(self.c_name, volumes = True, force = True)
            if result.get('status_code') != 204:
                print 'Remove container FAIL : ' + result.get('status_code')
        else:
            print 'Stop container FAIL : ' + result.get('status_code')

        