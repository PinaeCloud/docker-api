# coding=utf-8

from docker import session
from docker import host

s = session.get_session('http://192.168.228.130:2375')
h = host.Host(s)

print h.get_info()
print h.get_version()
