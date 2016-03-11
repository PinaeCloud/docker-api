# coding=utf-8

from docker import container_config

print_text = True
print_json = True

session_url = 'unix://var/run/docker.sock'

container_name = 'test-container'
image_name = 'alpine-ssh'
image_version = 'latest'

def get_container():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('interhui/alpine-ssh:latest')
    c_cfg.set_command('/usr/sbin/sshd -D')
    return c_cfg

def get_container_with_archive():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('interhui/alpine-ssh:latest')
    c_cfg.set_command(['/bin/sh', '-c'])
    return c_cfg

def get_container_with_log():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('interhui/alpine-ssh:latest')
    c_cfg.set_command(['/bin/sh', '-c', 'echo container log'])
    return c_cfg

def get_container_with_stdin():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('interhui/alpine-ssh:latest')
    c_cfg.set_stdin(True)
    c_cfg.set_command(['cat'])
    return c_cfg