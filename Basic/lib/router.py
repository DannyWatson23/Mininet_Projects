from mininet.net import Mininet
from lib.device import Device
import time
from mininet.log import setLogLevel, info
class Router(Device):
    print("Created Router")
    def __init__(self, clusternum, interface_info, net_obj, loopback_ip=''):
        self.clusternum = clusternum
        self.interface_info = interface_info
        self.ext_int = self.find_ext_int()
        self.loopback_ip = loopback_ip
        self.net_obj = net_obj
        self.host = ''
        self.host = self.net_obj.addHost('r'+str(self.clusternum))
        super().__init__(self.net_obj, self.host, self.clusternum, self.interface_info, 'router', self.loopback_ip)
        self.set_up_forwarding()
    def find_ext_int(self):
        for i in self.interface_info:
            if i['ext']:
                return 'r'+self.clusternum+'-'+i['interface']
    def set_up_default_ext_route(self, adj_ip):
        self.host.cmd('ip r a default via '+adj_ip+' dev '+self.interfacelist[0]['eth0'])
    def set_up_forwarding(self):
        self.host.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
