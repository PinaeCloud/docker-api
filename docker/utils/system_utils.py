# coding=utf-8

import os
import platform

def get_docker_fs(base_path):
    fs_types = ['aufs', 'devicemapper']
    for fs_type in fs_types:
        if os.path.exists(os.path.join(base_path, fs_type)):
            return fs_type
    return 'unknown'

def get_sys_info():
    system = {
              'hostname' : platform.node(),
              'system'  : platform.system(),
              'machine' : platform.machine(),
              'architecture' : platform.architecture(),
              'release' : platform.release(),
              'dist' : platform.dist(),
              'python' : platform.python_version()
              }
    return system

        
        