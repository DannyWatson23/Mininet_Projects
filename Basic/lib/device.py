from mininet.link import Link
from mininet.log import setLogLevel, info
import sys
class Device:
    print("Created device")
    def __init__(self, net_obj, dev_obj, cluster_num, interfaces, name, loopback_ip):
        self.net_obj = net_obj
        self.dev_obj = ''
        self.dev_obj = dev_obj
        self.cluster_num = cluster_num
        self.interfaces = interfaces
        interfacelist = list()
        interfacelist_data = {}
        self.loopback_ip = loopback_ip
        self.name = name        
        if 'outer' in self.name or 'OUTER' in self.name:
            self.type = 'Router'
            self.id = 'r'
        elif 'witch' in self.name or 'WITCH' in self.name:
            self.type = 'Switch'
            self.id = 'sw'
        elif 'ost' in self.name or 'OST' in self.name:
            self.type = 'Host'
            self.id = 'h'
        else:
            self.type = 'UNKNOWN'
        for i in self.interfaces:
            interfacelist_data[i['interface']] = self.id+self.cluster_num+'-'+i['interface']
            interfacelist.append(interfacelist_data)
        self.interfacelist = interfacelist
        #self.__str__()
    def initialise(self):
        self.set_up_links()
        self.set_up_loopback()
    def set_up_links(self):
        for i in self.interfaces:
            interface_name = self.id+self.cluster_num+'-'+i['interface']
            interface_ip = i['ip']
            interface_netmask = i['netmask']
            self.instatiate_interface(interface_name)
            self.set_ip_for_link(interface_name, interface_ip, interface_netmask)
    def instatiate_interface(self, interface_name):
        self.dev_obj.cmd('ifconfig '+interface_name+' 0')
    def set_ip_for_link(self, interface_name, interface_ip, interface_netmask):
        print(interface_name)
        self.dev_obj.cmd('ifconfig '+interface_name+' '+interface_ip+' netmask '+interface_netmask)
    def set_up_loopback(self):
        self.dev_obj.cmd('ifconfig lo '+self.loopback_ip+' netmask 255.255.255.255')
    def set_up_route(self, cmd):
        self.dev_obj.cmd(cmd)
    def connect_devices(self, a_obj, b_obj, net_obj, link1, link2):
        print("Connecting: "+str(link1)+ " to: "+str(link2))
        net_obj.addLink(a_obj.host, b_obj.host, intfName1 = link1, intfName2 = link2)
    def __str__(self):
        print(str(self.net_obj))
        print(self.cluster_num)
        print(self.interfaces)
        print(self.loopback_ip)
        print(self.name)
        print(self.type)
        print(str(self.dev_obj))

