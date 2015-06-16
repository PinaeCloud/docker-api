# coding=utf-8

from docker import session
from docker import container
from docker import container_config

#s = session.get_session('unix://var/run/docker.sock')
s = session.get_session('http://192.168.228.130:2375')
i = container.Container(s)

container_name = 'test_container'
# set host config
host_config = container_config.get_host_config('test_container')
# set host resource limit config
res_config = container_config.get_resource_config()
# set network config
net_config = container_config.get_net_config()
# set running config
run_config = container_config.get_run_config(['/usr/sbin/sshd', '-D'])

response = i.create(container_name, 'ubuntu-python', host_config, res_config, net_config, run_config)
conainer_id = response.get('Id')
print 'docker id is %s' % conainer_id
response = i.start(container_name)

response = i.list(None, True)

print response
