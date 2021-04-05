from mininet.net import Mininet
from lib.device import Device
import time
import sys
from mininet.log import setLogLevel, info
from mininet.nodelib import LinuxBridge
from mininet.node import UserSwitch

class Switch(Device):
    def __init__(self, clusternum, interface_info, net_obj):
        self.clusternum = clusternum
        self.interface_info = interface_info
        print(self.interface_info)
        self.net_obj = net_obj
        super().__init__(self.net_obj, self.clusternum, self.interface_info, 'switch')
        self.host = self.net_obj.addSwitch(self.id, cls=UserSwitch)
        for i in interface_info:
            if 'netw' in str(i):
                print(i)
                self.set_up_route('ip r a default via '+i['netw']+' dev '+self.interfacelist[0]['eth0'], self.host)