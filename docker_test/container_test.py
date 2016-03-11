# coding=utf-8

import unittest
import json
import os
import os.path
import tempfile

from docker.utils import tar_utils

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
                    self.fail('Start container FAIL : ' + str(result.get('status_code')))
            else:
                self.fail('Create container FAIL : ' + str(result.get('status_code')))
                
    def tearDown(self):
        result = self.c.stop(self.c_name)
        if result.get('status_code') == 204:
            result = self.c.remove(self.c_name, volumes = True, force = True)
            if result.get('status_code') != 204:
                self.fail('Remove container FAIL : ' + str(result.get('status_code')))
        else:
            self.fail('Stop container FAIL : ' + str(result.get('status_code')))
        
    def test_list(self):
        c_list = self.c.list(True, True)
        status_code = c_list.get('status_code')
        if status_code == 200:
            self.assertEqual(len(c_list.get('content')), 1)
            c_cfg = c_list.get('content')[0]
            self.assertIsNotNone(c_cfg.get('Id'))
            self.assertTrue(c_cfg.get('Status').startswith('Up'))
            self.assertTrue(c_cfg.get('Image'), 'interhui/alpine-ssh')
        else:
            self.fail('list : not any container, status_code :' + str(status_code))
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
            self.fail('inspect : not container {0}, status_code : {1}'.format(self.c_name, str(status_code)))
        if base_test.print_json:
            print 'inspect : ' + json.dumps(c_inspect)
        
    def test_status(self):
        c_status = self.c.status(self.c_name)
        status_code = c_status.get('status_code')
        if status_code == 200:
            content = c_status.get('content')
            self.assertIsNotNone(content.get('read'))
            self.assertTrue(content.get('memory_stats').get('usage') > 0)
            self.assertTrue(content.get('cpu_stats').get('cpu_usage').get('total_usage') > 0)
        else:
            self.fail('status : not container {0} or {0} not running, status_code : {1}'.format(self.c_name, str(status_code)))
        if base_test.print_json:
            print 'status:' + json.dumps(c_status)
        
    def test_top(self):
        c_tops = self.c.top(self.c_name)
        status_code = c_tops.get('status_code')
        if status_code == 200:
            processes = c_tops.get('content').get('Processes')
            self.assertEqual(len(processes), 1)
            self.assertEqual(processes[0][0], 'root')
            self.assertEqual(processes[0][7], '/usr/sbin/sshd -D')
        else:
            self.fail('top : not container {0} or {0} not running, status_code : {1}'.format(self.c_name, str(status_code)))
        if base_test.print_json:
            print 'top:' + json.dumps(c_tops)

    def test_layer(self):
        c_layer = self.c.layer(self.c_name)
        self.assertEqual(len(c_layer.get('content')), 4)
        if base_test.print_json:
            print 'layer:' + json.dumps(c_layer)
            
    def test_export(self):
        export_file = '/tmp/export-container.tar'
        c_export = self.c.export(base_test.container_name, export_file)
        status_code = c_export.get('status_code')
        if status_code == 200:
            self.assertEqual(c_export.get('content'), export_file)
            self.assertTrue(os.path.exists(export_file))
        else:
            self.fail('export : export {0} to {1} fail, status_code : {2}'.format(self.c_name, export_file, str(status_code)))
        if os.path.exists(export_file):
            os.remove(export_file)
        if base_test.print_json:
            print 'export:' + json.dumps(c_export)
            
class ContainerManageTest(unittest.TestCase):
    def __init__(self):
        pass
            
class ContainerArchiveTest(unittest.TestCase):
    
    def setUp(self):
        self.c_name = base_test.container_name
        
        self.c_session = session.get_session(base_test.session_url)
        self.c = container.Container(self.c_session)
        
        c_cfg = self.c.status(self.c_name)
        if c_cfg.get('status_code') != 200:
            c_cfg = base_test.get_container_with_archive()
            result = self.c.create(self.c_name, c_cfg)
            if result.get('status_code') == 201:
                result = self.c.start(self.c_name)
                if result.get('status_code') != 204:
                    self.fail('Start container FAIL : ' + str(result.get('status_code')))
            else:
                self.fail('Create container FAIL : ' + str(result.get('status_code')))
                
    def tearDown(self):
        result = self.c.remove(self.c_name, volumes = True, force = True)
        if result.get('status_code') != 204:
            self.fail('Remove container FAIL : ' + str(result.get('status_code')))
            
    def test_get_archive(self):
            tar_data, stat_data = self.c.get_archive(self.c_name, '/etc/hostname')
            with tempfile.NamedTemporaryFile() as tmp_tar_file:
                for chunk in tar_data:
                    tmp_tar_file.write(chunk)
                tmp_tar_file.seek(0)
                hostname = tar_utils.untar(tmp_tar_file, None, 'hostname')
                self.assertGreater(len(hostname), 0)
                if base_test.print_text:
                    print 'get_archive:' + json.dumps(stat_data)
                    
    def test_put_archive(self):
        tar_data = tar_utils.tar(['/etc/hostname'])
        c_archive = self.c.put_archive(self.c_name, '/root/', tar_data)
        if c_archive.get('status_code') == 200:
            tar_data, stat_data = self.c.get_archive(self.c_name, '/root/etc/hostname')
            with tempfile.NamedTemporaryFile() as tmp_tar_file:
                for chunk in tar_data:
                    tmp_tar_file.write(chunk)
                tmp_tar_file.seek(0)
                hostname = tar_utils.untar(tmp_tar_file, None, 'hostname')
                self.assertGreater(len(hostname), 0)
                if base_test.print_text:
                    print 'put_archive:' + json.dumps(stat_data)
  
class ContainerExecTest(unittest.TestCase):
    
    def setUp(self):
        self.c_name = base_test.container_name
        
        self.c_session = session.get_session(base_test.session_url)
        self.c = container.Container(self.c_session)
        
        c_cfg = self.c.status(self.c_name)
        if c_cfg.get('status_code') != 200:
            c_cfg = base_test.get_container_with_stdin()
            result = self.c.create(self.c_name, c_cfg)
            if result.get('status_code') == 201:
                result = self.c.start(self.c_name)
                if result.get('status_code') != 204:
                    self.fail('Start container FAIL : ' + str(result.get('status_code')))
            else:
                self.fail('Create container FAIL : ' + str(result.get('status_code')))
                
    def tearDown(self):
        result = self.c.stop(self.c_name)
        if result.get('status_code') == 204:
            result = self.c.remove(self.c_name, volumes = True, force = True)
            if result.get('status_code') != 204:
                self.fail('Remove container FAIL : ' + str(result.get('status_code')))
        else:
            self.fail('Stop container FAIL : ' + str(result.get('status_code')))
            
    def test_exec(self):
        c_exec = self.c.exec_create(self.c_name, ['echo', 'exec test'])
        if c_exec.get('status_code') == 201:
            exec_id = c_exec.get('content').get('Id')
            self.assertIsNotNone(exec_id)
            
            if base_test.print_json:
                print 'exec create:' + json.dumps(c_exec)
            
            inspect_result = self.c.exec_inspect(exec_id)
            if inspect_result.get('status_code') == 200:
                inspect_content = inspect_result.get('content')
                self.assertEquals(inspect_content.get('ID'), exec_id)
            if base_test.print_json:
                print 'exec inspect:' + json.dumps(inspect_result)
            exec_result = self.c.exec_start(exec_id)
            if exec_result.get('status_code') == 200:
                self.assertTrue('exec test' in exec_result.get('content'))
            if base_test.print_json:
                print 'exec start:' + json.dumps(exec_result)
            else:
                self.fail('Start exec FAIL : ' + str(exec_result.get('status_code')))
            
        else:
            self.fail('Create exec FAIL : ' + str(c_exec.get('status_code')))
        

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
                if result.get('status_code') == 204:
                    self.c.wait(self.c_name)
                else:
                    self.fail('Start container FAIL : ' + str(result.get('status_code')))
            else:
                self.fail('Create container FAIL : ' + str(result.get('status_code')))
                
    def tearDown(self):
        result = self.c.remove(self.c_name, volumes = True, force = True)
        if result.get('status_code') != 204:
            self.fail('Remove container FAIL : ' + str(result.get('status_code')))
    
    def test_logs(self):
        logs = self.c.logs(self.c_name)
        self.assertGreater(len(logs.get('content')), 0)
        if base_test.print_json:
            print 'logs:' + json.dumps(logs)

    def test_logs_with_stream(self):
        logs = []
        for log_str in self.c.logs_stream(self.c_name):
            logs.append(log_str)
            if len(logs) > 0:
                break 
        self.assertEquals(len(logs), 1)
        if base_test.print_text:
            print 'logs_stream:' + str(logs)
        
    def test_logs_local(self):
        logs = self.c.logs_local(self.c_name, True, True, '2016-03-01 00:00:00')
        self.assertEquals(len(logs.get('content')), 1)
        if base_test.print_json:
            print 'logs_local:' + json.dumps(logs)


        