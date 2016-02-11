# coding=utf-8

import json
#from docker import session
#from docker import container
from docker import container_config

#s = session.get_session('unix://var/run/docker.sock')
#s = session.get_session('http://192.168.228.130:2375')
#i = container.Container(s)

new_container = container_config.ContainerConfig()
new_container.set_image('ubuntu:14.04')
new_container.set_hostname('test-container', 'workgroup')
new_container.set_tty(True)
new_container.set_attach(False, True, True)
new_container.set_privileged(True)
new_container.set_cpu(2, 512)
new_container.set_memory(262144, 524288)
new_container.set_user('docker')
new_container.set_workdir('/root')

new_container.set_command('/bin/bash')

new_container.enable_network(True)

new_container.add_bind_port(22, 'tcp', None, 2202)
new_container.add_bind_port(21, 'tcp', None, 21)
new_container.add_bind_port(3306, 'tcp', None, None)

new_container.add_device('/dev/sda1', '/dev/sda1', 'mrw')
new_container.add_device('/dev/fp0', '/dev/fp0', 'mrw')

new_container.add_dns('192.168.199.2')
new_container.add_dns('8.8.8.8')

new_container.add_hosts('localhost', '127.0.0.1')
new_container.add_hosts('test-container', '127.0.0.1')

new_container.add_label('version', '1.0')
new_container.add_label('author', 'Huiyugeng')

new_container.add_env('WORKING_DIR', '/root')
new_container.add_env('PACKAGE_DIR', '/opt/package')

config = new_container.get_config()
print json.dumps(config)

