from mininet.link import Link
from mininet.log import setLogLevel, info
import sys

dev_list = list()

class Device:
    print("Created device")
    def __init__(self, net_obj, cluster_num, interfaces, name):
        self.net_obj = net_obj
        self.cluster_num = cluster_num
        self.interfaces = interfaces
        self.dev_obj = ''
        interfacelist = list()
        interfacelist_data = {}
        self.loopback_ip = self.find_loopback()
        self.name = name
        if 'outer' in self.name or 'OUTER' in self.name:
            rcount=1
            for i in dev_list:
                if i[3] in self.name:
                    rcount+=1
            self.type = 'Router'
            self.id = 'r'+str(rcount)
        elif 'witch' in self.name or 'WITCH' in self.name:
            scount=1
            for i in dev_list:
                if i[3] in self.name:
                    scount+=1
            self.type = 'Switch'
            self.id = 'sw'+str(scount)
        elif 'ost' in self.name or 'OST' in self.name:
            hcount=1
            for i in dev_list:
                if i[3] in self.name:
                    hcount+=1
            self.type = 'Host'
            self.id = 'h'+str(hcount)
        else:
            self.type = 'UNKNOWN'
        for i in self.interfaces:
            interfacelist_data[i['interface']] = self.id+'-'+i['interface']
            interfacelist.append(interfacelist_data)
        self.interfacelist = interfacelist
        dev = self.cluster_num, self.interfaces, self.loopback_ip, self.name, self.type, self.net_obj
        dev_list.append(dev)
        #self.__str__()
    def find_loopback(self):
        for i in self.interfaces:
            if i['interface'] == 'lo':
                return i['ip']
        return 'x'
    def initialise(self, dev_obj):
        self.dev_obj = dev_obj
        self.set_up_links()
        self.set_up_loopback()
    def set_up_links(self):
        for i in self.interfaces:
            interface_name = self.id+'-'+i['interface']
            print(i)
            if 'ip' in str(i):
                interface_ip = i['ip']
                if i['interface'] == 'lo':
                    interface_netmask = '255.255.255.255'
                else:
                    interface_netmask = i['netmask']
                self.instatiate_interface(interface_name)
                self.set_ip_for_link(interface_name, interface_ip, interface_netmask)
            else:
                print("switch")
                # Some devices like switches don't have IPs for interfaces
                self.instatiate_interface(interface_name)
    def instatiate_interface(self, interface_name):
        self.dev_obj.cmd('ifconfig '+interface_name+' 0')
    def set_ip_for_link(self, interface_name, interface_ip, interface_netmask):
        print(interface_name)
        self.dev_obj.cmd('ifconfig '+interface_name+' '+interface_ip+' netmask '+interface_netmask)
    def set_up_loopback(self):
        if self.loopback_ip != 'x':
            self.dev_obj.cmd('ifconfig lo '+self.loopback_ip+' netmask 255.255.255.255')
    def set_up_route(self, cmd, dev_obj):
        dev_obj.cmd(cmd)
    def execute(self, cmd):
        self.dev_obj.cmd(cmd)
    def connect_devices(self, a_obj, b_obj, net_obj, link1, link2):
        print("Connecting: "+str(link1)+ " to: "+str(link2))
        net_obj.addLink(a_obj.host, b_obj.host, intfName1 = link1, intfName2 = link2)
    def __str__(self):
        print(self.cluster_num)
        print(self.interfaces)
        print(self.loopback_ip)
        print(self.name)
        print(self.type)
        print(str(self.dev_obj))

