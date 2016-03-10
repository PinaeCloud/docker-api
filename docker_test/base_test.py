# coding=utf-8

from docker import container_config

print_text = True
print_json = True

session_url = 'unix://var/run/docker.sock'

container_name = 'test-container'
image_name = 'ubuntu'
image_version = '14.04'

def get_container():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('interhui/openssh:latest')
    c_cfg.set_command('/usr/sbin/sshd -D')
    return c_cfg

def get_container_with_log():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('ubuntu:14.04')
    c_cfg.set_command(['/bin/bash', '-c', 'echo container log'])
    return c_cfg

def get_container_with_stdin():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('ubuntu:14.04')
    c_cfg.set_stdin(True)
    c_cfg.set_command(['cat'])
    return c_cfg