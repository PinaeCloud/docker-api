# coding=utf-8

from docker import session
from docker import container
from docker import version

#s = session.get_session('unix://var/run/docker.sock')
s = session.get_session('http://192.168.228.130:2375')
i = container.Container(s)

#container_name = 'test_container'
#response = i.create(container_name, container_name, 'ubuntu-python', ['/usr/sbin/sshd', '-D'])
#conainer_id = response.get('Id')
#print 'docker id is %s' % conainer_id
#response = i.start(container_name)

#response = i.list(None, True)

response = version.get_version(s)
print response
