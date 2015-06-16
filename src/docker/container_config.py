# coding=utf-8

import types

def __get_config(image, host_config, res_config, net_config, run_config):
    
    config = {
        'Hostname': host_config.get('hostname'),
        'Image': image,
        'Cmd' : run_config.get('cmd')
        }
    return config

def get_host_config(hostname = None, domainname = None, labels = None, user = None, volumn = None, device = None, ulimit = None, log = None):
    host_config = {}
    
    if hostname != None and type(hostname) == types.StringType:
        host_config['hostname'] = hostname
    if domainname != None and type(domainname) == types.StringType:
        host_config['domainname'] = domainname
    if user != None and type(user) == types.StringType:
        host_config['user'] = user
    
    host_config['labels'] = labels if labels != None else None
    
    host_config['volumn'] = volumn if volumn != None else None
    host_config['device'] = device if device != None else None
    
    host_config['ulimit'] = ulimit if ulimit != None else None
    host_config['log'] = log if log != None else None
    
    return host_config

def get_resource_config(cpu_count = None, cpu_limit = None, memory = None, memory_swap = None, io = None):
    return {}

def get_net_config(enable, mode = None, interfaces = None, dns = None, bind_ports = None, hosts = None):
    return {}

def get_run_config(cmd = None, env= None, working_dir = None, labels = None, link = None, tty = None, attach = None):
    run_config = {
        'cmd' : cmd
        }
    return run_config