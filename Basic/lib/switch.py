from mininet.net import Mininet
from lib.device import Device
import time
import sys
from mininet.log import setLogLevel, info
from mininet.nodelib import LinuxBridge

class Switch(Device):
    def __init__(self, clusternum, interface_info, net_obj, loopback_ip=''):
        self.clusternum = clusternum
        self.interface_info = interface_info
        self.loopback_ip = loopback_ip
        self.net_obj = net_obj
        self.host = self.net_obj.addSwitch('sw'+str(self.clusternum), cls=LinuxBridge)
        super().__init__(self.net_obj, self.host, self.clusternum, self.interface_info, 'switch', self.loopback_ip)