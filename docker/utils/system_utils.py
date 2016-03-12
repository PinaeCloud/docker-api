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
    pass

def mount(fs_type, dev_list, mnt_point):
    pass
        
        