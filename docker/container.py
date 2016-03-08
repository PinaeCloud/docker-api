# coding=utf-8

import json
import types
import time

from utils import time_utils
from docker import container_config
from text import string_utils as str_utils

class Container():
    def __init__(self, session):
        self.session = session
 
    def list(self, container_id = None, show_all = False, show_size = False, status = None, labels = None, exit_code = None):
        params = {}
        params['all'] = True if show_all is True else False
        params['size'] = True if show_size is True else False
        
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
    
    def inspect(self, container_id):
        url = self.session._url('/containers/{0}/json'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def status(self, container_id):
        url = self.session._url('/containers/{0}/stats'.format(container_id))
        response = self.session._result(self.session._get(url, params={'stream': False}))
        return response

    def top(self, container_id):
        url = self.session._url('/containers/{0}/top'.format(container_id))
        response = self.session._result(self.session._get(url, params={}))
        return response
    
    def logs(self, container_id, stdout = True, stderr = True, stream = False,
             timestamps = False, tail = 'all', since = None):
        params = {'stderr': stderr and 1 or 0,
                  'stdout': stdout and 1 or 0,
                  'timestamps': timestamps and 1 or 0,
                  'follow': stream and 1 or 0,
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
    
    def logs_stream(self, container_id, stdout = True, stderr = True, timestamps = False, since = None):
        response = self.logs(container_id, stdout, stderr, True, timestamps, 'all', since)
        
        log = ''
        for chunk in response:
            log = log + chunk
            if chunk == '\n':
                log = log.strip()
                yield log
                log = ''
                
    def logs_local(self, container_id, stdout = True, stderr = True, since = None):
        container = self.inspect(container_id)
        if container.get('status_code') == 200:
            container_id = container['content']['Id']
            log_list = self.session._read('/containers/{0}/{0}-json.log'.format(container_id))
            if log_list is not None:
                result = []
                for log_str in log_list:
                    log = json.loads(log_str)
                    stream = log.get('stream')
                    
                    is_match = False
                    if (stdout is True and stream == 'stdout') or (stderr is True and stream == 'stderr'):
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
                    return result
        return None
    
    def layer(self, container_id):
        layers = []
        
        def recurse_layer(mount_ids):
            if mount_ids != None and len(mount_ids) > 0:
                for mount_id in mount_ids:
                    if mount_id not in layers:
                        layers.append(mount_id)
                    recurse_layer(self.session._read('/aufs/layers/{0}'.format(mount_id)))
        
        container = self.inspect(container_id)
        if container.get('status_code') == 200:
            container_id = container['content']['Id']
            
            mount_id = self.session._read('/image/aufs/layerdb/mounts/{0}/mount-id'.format(container_id))
            if mount_id != None:
                recurse_layer(mount_id)
                
            return layers
    
    def create(self, name, container_cfg):
        params = {}
        if isinstance(container_cfg, container_config.ContainerConfig):
            container_cfg = container_cfg.build_config()
        if str_utils.is_not_empty(name):
            params['name'] = name
        url = self.session._url('/containers/create')
        response = self.session._result(self.session._post_json(url, data=container_cfg, params=params))
        return response
    
    def rename(self, container_id, new_name):
        if new_name:
            params = {'name' : new_name}
        url = self.session._url('/containers/{0}/rename'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response

    def remove(self, container_id, volumes = False, force = False):
        params = {}
        params['v'] = True if volumes is True else False
        params['force'] = True if force is True else False
        url = self.session._url('/containers/{0}'.format(container_id))
        response = self.session._result(self.session._delete(url, params=params))
        return response
    
    def start(self, container_id):
        url = self.session._url('/containers/{0}/start'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def stop(self, container_id, wait = None):
        params = {}
        if wait:
            params['t'] = wait
        url = self.session._url('/containers/{0}/stop'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response

    def restart(self, container_id, wait = None):
        params = {}
        if wait:
            params['t'] = wait
        url = self.session._url('/containers/{0}/restart'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response
    
    def kill(self, container_id, signal = None):
        params = {}
        if signal:
            params['signal'] = signal
        url = self.session._url('/containers/{0}/kill'.format(container_id))
        response = self.session._result(self.session._post(url, params=params))
        return response
    
    def pause(self, container_id):
        url = self.session._url('/containers/{0}/pause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def unpause(self, container_id):
        url = self.session._url('/containers/{0}/unpause'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def wait(self, container_id):
        url = self.session._url('/containers/{0}/wait'.format(container_id))
        response = self.session._result(self.session._post(url, params={}))
        return response
    
    def update(self, container_id, resource):
        if resource is None:
            raise IOError('resource is Empty')
        url = self.session._url('/containers/{0}/update'.format(container_id))
        response = self.session._result(self.session._post(url, data=resource, params={}))
        return response
    
    def commit(self, container_id, repository, tag = None, authot = None, comment = None, pause = False):
        pass
    
    def export(self, container_id, filename):
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
                'content-type' : 'text/plain',
                'content' : filename
                }
                
