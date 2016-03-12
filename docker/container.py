# coding=utf-8

import json
import logging
import types
import time
import base64

from docker.utils import time_utils
from docker.utils import tar_utils
from docker.utils import system_utils
from docker.utils import decorators 
from docker import container_config
from text import string_utils as str_utils

log = logging.getLogger(__name__)

class Container():
    def __init__(self, session):
        self.session = session
 
    def list(self, container_id = None, show_all = False, show_size = False, status = None, labels = None, exit_code = None):
        params = {}
        params['all'] = show_all and True or False
        params['size'] = show_size and True or False
        
        filters = {}
        if status is not None:
            filters['status'] = status
        if labels is not None:
            if type(labels) == types.DictionaryType:
                filters['label'] = labels
            else:
                raise TypeError('container label must be a dict')
        if exit_code is not None:
            filters['exit_code'] = exit_code
            
        if len(filters) > 0:
            params['filters'] = filters
            
        url = self.session._url('/containers/json')
        response = self.session._result(self.session._get(url, params=params))
        return response
    
    @decorators.check_container
    def inspect(self, container_id):
        url = self.session._url('/containers/{0}/json'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    @decorators.check_container
    def status(self, container_id):
        url = self.session._url('/containers/{0}/stats'.format(container_id))
        response = self.session._result(self.session._get(url, params={'stream': False}))
        return response
    
    @decorators.check_container
    def top(self, container_id):
        url = self.session._url('/containers/{0}/top'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    @decorators.check_container
    def logs(self, container_id, stdout = True, stderr = True, stream = False,
             timestamps = False, tail = 'all', since = None):
        params = {'stderr': stderr,
                  'stdout': stdout,
                  'timestamps': timestamps,
                  'follow': stream,
                  'tail': tail,
                  'since': since
                }
        url = self.session._url('/containers/{0}/logs'.format(container_id))
        response = self.session._result(self.session._get(url, params=params, stream=stream), stream)
        if stream is False and response.get('status_code') == 200:
            content = response.get('content')
            log_list = [log.strip() for log in content.split('\n')]
            response['content'] = log_list
        return response
    
    @decorators.check_container
    def logs_stream(self, container_id, stdout = True, stderr = True, timestamps = False, since = None):
        response = self.logs(container_id, stdout, stderr, True, timestamps, 'all', since)
        
        log_str = ''
        for chunk in response:
            log_str = log_str + str(chunk.encode("utf-8")) 
            if chunk == '\n':
                log_str = log_str.strip()
                yield log_str
                log_str = ''
                
    @decorators.check_container
    def logs_local(self, container_id, stdout = True, stderr = True, since = None):
        container = self.inspect(container_id)
        status_code = container.get('status_code')
        if status_code == 200:
            container_id = container['content']['Id']
            log_list = self.session._read('/containers/{0}/{0}-json.log'.format(container_id))
            if log_list is not None:
                result = []
                for log_str in log_list:
                    log = json.loads(log_str)
                    stream = log.get('stream')
                    
                    is_match = False
                    if (stdout and stream == 'stdout') or (stderr and stream == 'stderr'):
                        is_match = True

                    if since is not None:
                        since = time_utils.parse_time(since)
                            
                        if isinstance(since, time.struct_time):
                            try:
                                timestamps = log.get('time')
                                # 日期格式为%Y-%m-%dT%H:%M:%S.%MSZ, 需要将毫秒进行清理
                                timestamps = timestamps.split('.')[0]
                                log_time = time.mktime(time.strptime(timestamps, '%Y-%m-%dT%H:%M:%S'))
                                since_time = time.mktime(since)
                                is_match =  True if log_time > since_time else False
                            except:
                                is_match = False
                            
                    if is_match:
                        result.append(log)
                        
                if len(result) > 0:
                    return {'status_code' : 200, 'content' : result}
                
        return {'status_code' : status_code}
    
    @decorators.check_container
    def layer(self, container_id):     
        layers = []
        def recurse_layer(mount_ids):
            if mount_ids != None and len(mount_ids) > 0:
                for mount_id in mount_ids:
                    if mount_id not in layers:
                        layers.append(mount_id)
                    recurse_layer(self.session._read('/aufs/layers/{0}'.format(mount_id)))
        
        container = self.inspect(container_id)
        status_code = container.get('status_code')
        if status_code == 200:
            container_id = container['content']['Id']
            
            mount_id = self.session._read('/image/aufs/layerdb/mounts/{0}/mount-id'.format(container_id))
            if mount_id != None:
                fs_type = system_utils.get_docker_fs(self.session._get_docker_path())
                if fs_type == 'aufs':
                    recurse_layer(mount_id)
                elif fs_type == 'mapper':
                    layers.append(mount_id)
                else:
                    return {'status_code' : 500, 'content' : 'Unknown docker filesystem'}
            return {'status_code' : 200, 'content' : layers}
        else:
            return {'status_code' : status_code}
    
    def create(self, name, container_cfg):
        params = {}
        if isinstance(container_cfg, container_config.ContainerConfig):
            container_cfg = container_cfg.build_config()
        if str_utils.is_not_empty(name):
            params['name'] = name
        url = self.session._url('/containers/create')
        response = self.session._result(self.session._post_json(url, data=container_cfg, params=params))
        return response
    
    @decorators.check_container
    def rename(self, container_id, new_name):
        if str_utils.is_empty(new_name):
            raise ValueError('New container name is empty')
        if new_name:
            params = {'name' : new_name}
        url = self.session._url('/containers/{0}/rename'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response

    @decorators.check_container
    def remove(self, container_id, volumes = False, force = False):
        params = {}
        params['v'] = volumes and True or False
        params['force'] = force and True or False
        url = self.session._url('/containers/{0}'.format(container_id))
        response = self.session._result(self.session._delete(url, params=params))
        return response
    
    @decorators.check_container
    def start(self, container_id):
        url = self.session._url('/containers/{0}/start'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    @decorators.check_container
    def stop(self, container_id, wait = None):
        params = {}
        if wait:
            params['t'] = wait
        url = self.session._url('/containers/{0}/stop'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response

    @decorators.check_container
    def restart(self, container_id, wait = None):
        params = {}
        if wait:
            params['t'] = wait
        url = self.session._url('/containers/{0}/restart'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response
    
    @decorators.check_container
    def kill(self, container_id, signal = None):
        params = {}
        if signal:
            params['signal'] = signal
        url = self.session._url('/containers/{0}/kill'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response
    
    @decorators.check_container
    def pause(self, container_id):
        url = self.session._url('/containers/{0}/pause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    @decorators.check_container
    def unpause(self, container_id):
        url = self.session._url('/containers/{0}/unpause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    @decorators.check_container
    def wait(self, container_id):
        url = self.session._url('/containers/{0}/wait'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    @decorators.check_container
    def update(self, container_id, resource):
        if resource is None:
            raise ValueError('resource is empty')
        url = self.session._url('/containers/{0}/update'.format(container_id))
        response = self.session._result(self.session._post(url, data=resource, params={}))
        return response
    
    @decorators.check_container
    def resize(self, container_id, height = 40, width = 80):
        if not str_utils.is_numeric(height) or not str_utils.is_numeric(width):
            raise ValueError('height or width is NOT Numeric')
        params={'h' : height, 'w' : width}
        url = self.session._url('/containers/{0}/wait'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response
    
    
    @decorators.check_container
    def commit(self, container_id, repository, tag = None, author = None, comment = None, pause = False, config = None):
        params = {
            'container': container_id,
            'repo': repository,
            'tag': tag,
            'comment': comment,
            'author': author
                }
        u = self._url("/commit")
        return self._result(self._post_json(u, data=config, params=params),
                            json=True)
    
    @decorators.check_container
    def export(self, container_id, filename):
        if str_utils.is_empty(filename):
            raise ValueError('Export filename is empty')
        url = self.session._url('/containers/{0}/export'.format(container_id))
        response = self.session._get(url, params={}, stream=True)
        if response.status_code == 200:
            export_file = open(filename,'wb') 
            export_date = self.session._stream_raw_result(response, 2048)
            for chunk in export_date:
                export_file.write(chunk)
            export_file.close()
        return {
                'status_code' : response.status_code,
                'content' : filename
                }
        
    @decorators.check_container
    def exec_create(self, container_id, cmd, stdin = False, stdout = True, stderr = True, tty = False): 
        if str_utils.is_empty(cmd):
            raise ValueError('Exec cmd is empty')
        if isinstance(cmd, str):
            cmd = cmd.split(' ')
        data = {
            'AttachStdin': stdin,
            'AttachStdout': stdout,
            'AttachStderr': stderr,
            'Tty': tty,
            'Cmd': cmd
                }
        url = self.session._url('/containers/{0}/exec'.format(container_id))
        response = self.session._result(self.session._post_json(url, data=data, params={}))
        return response
    
    def exec_start(self, exec_id, detach = False, tty= False, stream = False):
        data = {
            'Detach': detach,
            'Tty': tty
                }
        url = self.session._url('/exec/{0}/start'.format(exec_id))
        response = self.session._result(self.session._post_json(url, data=data, params={}, stream=stream), stream)
        return response
    
    def exec_resize(self, exec_id, height = 40, width = 80):
        params = {
            'h': height,
            'w': width
                }
        url = self.session._url('/exec/{0}/resize'.format(exec_id))
        response = self.session._result(self.session._get(url, params=params))
        return response

    def exec_inspect(self, exec_id):
        url = self.session._url('/exec/{0}/json'.format(exec_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    @decorators.check_container
    def get_archive(self, container_id, path):
        params = {'path' : path}
        url = self.session._url('/containers/{0}/archive'.format(container_id))
        response = self.session._get(url, params = params, stream = True)
        if response.status_code == 200:
            encoded_stat = response.headers.get('x-docker-container-path-stat')
            stat_data = json.loads(base64.b64decode(encoded_stat)) if encoded_stat is not None else None 
            return response.raw, stat_data
        else:
            return {'status_code', response.status_code}, None
    
    @decorators.check_container
    def put_archive(self, container_id, path, tar_data, overwrite = False):
        params = {
                  'path': path, 
                  'noOverwriteDirNonDir' : overwrite
                  }
        if isinstance(tar_data, str):
            tar_data = tar_utils.tar(tar_data)
        url = self.session._url('/containers/{0}/archive'.format(container_id))
        response = self.session._put(url, params = params, data = tar_data)
        return {'status_code' : response.status_code}
        
        