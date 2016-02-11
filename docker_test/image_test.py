# coding=utf-8

from docker import session
from docker import image

#s = dsession.get_session('unix://var/run/docker.sock')
s = session.Session('http://192.168.228.130:2375')
i = image.Image(s)
print i.list()