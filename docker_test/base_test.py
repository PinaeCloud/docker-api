# coding=utf-8

from docker import container_config

session_url = 'http://192.168.228.129:2375'
container_name = 'test-container'
image_name = 'ubuntu'
image_version = '14.04'

def get_container():
    c_cfg = container_config.ContainerConfig()
    c_cfg.set_image('interhui/openssh:latest')
    c_cfg.set_command('/usr/sbin/sshd -D')
    