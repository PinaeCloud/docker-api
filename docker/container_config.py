# coding=utf-8

from docker.utils import string_utils as str_utils
from docker.utils import regex_utils

class ContainerConfig():
    
    def __init__(self):
        self.config = {}
        
        self.container = {}
        self.resource = {}
        self.network = {}
        self.running = {}
        
        #默认激活网络
        self.network['network'] = True

    def build_config(self):
        
        # 容器配置定义
        self.__set_value('Image', self.container.get('image'))
        self.__set_value('Labels', self.container.get('label'))
        self.__set_value('HostConfig/Privileged', self.container.get('privileged'))
        self.__set_value('Entrypoint', self.container.get('entrypoint'))
        self.__set_value('Cmd', self.container.get('command'))
        
        # 资源配置定义
        self.__set_value('HostConfig/Devices', self.resource.get('device'))
        self.__set_value('HostConfig/Binds', self.resource.get('volume'))
        self.__set_value('HostConfig/Memory', self.resource.get('memory'))
        self.__set_value('HostConfig/CpusetCpus', self.resource.get('cpuset'))
        self.__set_value('HostConfig/CpuShares', self.resource.get('cpulimit'))
        
        # 网络配置定义
        self.__set_value('NetworkDisabled', (not self.network.get('network')))
        self.__set_value('HostConfig/Dns', self.network.get('dns'))
        self.__set_value('HostConfig/ExtraHosts', self.network.get('hosts'))
        self.__set_value('PublishAllPorts', self.network.get('allports'))
        self.__set_value('HostConfig/PortBindings', self.network.get('ports'))
            
        ports = self.network.get('ports')
        if ports != None:
            exposed_ports = {}
            for port in ports:
                exposed_ports[port] = {}
            self.config['ExposedPorts'] = exposed_ports
        
        # 运行配置定义
        self.__set_value('Hostname', self.running.get('hostname'))
        self.__set_value('Domainname', self.running.get('domain'))
        self.__set_value('User', self.running.get('user'))
        self.__set_value('WorkingDir', self.running.get('workdir'))
        self.__set_value('Env', self.running.get('environment'))
        self.__set_value('Tty', self.running.get('tty'))
        self.__set_value('AttachStdin', self.running.get('stdin'))
        self.__set_value('AttachStdout', self.running.get('stdout'))
        self.__set_value('AttachStderr', self.running.get('stderr'))
        self.__set_value('StdinOnce', self.running.get('stdinonce'))
        self.__set_value('OpenStdin', self.running.get('openstdin'))
        
        return self.config
    
    def set_image(self, image):
        if str_utils.is_not_empty(image):
            self.container['image'] = image
        else:
            raise 'Image is None'
    
    def set_hostname(self, hostname, domain = None):
        self.running['hostname'] = hostname
        if str_utils.is_not_empty(domain):
            self.running['domain'] = domain
        
    def set_user(self, user):
        if user != None:
            self.running['user'] = user
    
    def add_label(self, key, value):
        if str_utils.is_not_empty(key) and str_utils.is_not_empty(value):
            labels = self.container.get('label') if self.container.has_key('label') else {}
            labels[key] = value
            self.container['label'] = labels
    
    def set_cpu(self, cpu_count, cpu_limit):
        if cpu_count != None and str_utils.is_numeric(cpu_count):
            cpu_count = [str(i) for i in range(int(cpu_count))]
            self.resource['cpuset'] = ','.join(cpu_count)
        if cpu_limit != None and str_utils.is_numeric(cpu_limit):
            self.resource['cpulimit'] = cpu_limit
    
    def set_memory(self, memory, swap):
        if memory != None and str_utils.is_numeric(memory):
            self.resource['memory'] = int(memory) * 1024
            if swap != None and (swap == '-1' or str_utils.is_numeric(swap)):
                if int(swap) > int(memory):
                    self.resource['swap'] = int(swap) * 1024
    
    def add_device(self, host_device, container_device, permissions):
        if host_device != None and container_device != None and permissions != None:
            devices = self.resource.get('device') if self.resource.has_key('device') else []
            device = {
                      'PathOnHost' : host_device,
                      'PathInContainer' : container_device,
                      'CgroupPermissions' : permissions
                      }
            devices.append(device)
            self.resource['device'] = devices
    
    def add_volume(self, volume_name, container_path, read_only = False):
        if container_path != None:
            volume_list = self.resource.get('volume') if self.resource.has_key('volume') else []
            volume = container_path
            if volume_name != None:
                volume = volume_name + ':' + volume
            if read_only == True:
                volume = volume + ':ro'
            volume_list.append(volume)
            self.resource['volume'] = volume_list
            
    
    def enable_network(self, enable = True):
        self.network['network'] = enable
    
    def add_interface(self, bridge, mac, ip, netmask, gateway, vlan = None):
        pass
    
    def add_dns(self, dns):
        if str_utils.is_not_empty(dns) and regex_utils.check_line('\d+\.\d+\.\d+\.\d+', dns):
            dns_list = self.network.get('dns') if self.network.has_key('dns') else []
            dns_list.append(dns)
            self.network['dns'] = dns_list
            
    def bind_all_ports(self, bind = True):
        self.network['allports'] = bind
    
    def add_bind_port(self, container_port, protocol, host_ip = None, host_port = None):
        if container_port != None and protocol != None:
            container_port = str(container_port)
            if str_utils.is_numeric(container_port):
                if protocol == 'tcp' or protocol == 'udp':
                    ports = self.network.get('ports') if self.network.has_key('ports') else {}
                    port = str(container_port) + '/' + protocol
                    
                    host_ports = []
                    
                    if host_port == None:
                        host_port = container_port
                         
                    host_port = str(host_port)
                    
                    host_port_config = {'HostPort' : host_port}
                    if host_ip != None:
                        host_port_config['HostIp'] = host_ip
                            
                    host_ports.append(host_port_config)
                        
                    ports[port] = host_ports
                    self.network['ports'] = ports
        else:
            raise 'Port or Protocol is None'
                
    def add_hosts(self, hostname, ip):
        if str_utils.is_not_empty(hostname) and str_utils.is_not_empty(ip):
            hosts = self.network.get('hosts') if self.network.has_key('hosts') else []
            hosts.append(hostname + ':' + ip)
            self.network['hosts'] = hosts

    def set_privileged(self, privileged = True):
        self.container['privileged'] = privileged
    
    def add_entrypoint(self, entrypoint):
        if str_utils.is_not_empty(entrypoint):
            entrypoints = self.container.get('entrypoint') if self.container.has_key('entrypoint') else []
            entrypoints.append(entrypoint)
            self.container['entrypoint'] = entrypoints
            
    def set_command(self, command):
        if command != None and isinstance(command, list):
            self.container['command'] = command
        else:  
            self.container['command'] = command.split(' ')
    
    def set_workdir(self, workdir):
        if str_utils.is_not_empty(workdir):
            self.running['workdir'] = workdir
    
    def add_env(self, key, value):
        if str_utils.is_not_empty(key) and str_utils.is_not_empty(value):
            envs = self.running.get('environment') if self.running.has_key('environment') else []
            envs.append(key + '=' + value)
            self.running['environment'] = envs
    
    def set_tty(self, tty = True):
        self.running['tty'] = tty
    
    def set_attach(self, stdin = False, stdout = True, stderr = True):
        self.running['stdin'] = stdin
        self.running['stdout'] = stdout
        self.running['stderr'] = stderr
        if stdin:
            self.running['stdinonce'] = True
        
    def set_stdin(self, open_stdin = True):
        self.running['openstdin'] = open_stdin
        
    def __set_value(self, path, item):
        if item != None:
            path_items = path.split('/')
            path_items_len = len(path_items)
            
            current_node = self.config
            for index in range(path_items_len):
                path_item = path_items[index]
                if index + 1 < path_items_len:
                    if current_node.has_key(path_item) == False:
                        current_node[path_item] = {}
                    current_node = current_node.get(path_item)
                else:
                    current_node[path_item] = item
