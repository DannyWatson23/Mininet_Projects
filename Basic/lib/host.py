from mininet.net import Mininet
from lib.device import Device


class Host(Device):
    def __init__(self, clusternum, interface_info, net_obj, loopback_ip=''):
        self.clusternum = clusternum
        self.interface_info = interface_info
        self.loopback_ip = loopback_ip
        self.net_obj = net_obj
        self.host = self.net_obj.addHost('h'+str(self.clusternum))
        super().__init__(self.net_obj, self.host, self.clusternum, self.interface_info, 'host', self.loopback_ip)
    def set_up_default_route(self):
        self.host.cmd('route add default dev h'+self.clusternum+'-'+self.interface_info[0]['interface'])        
        print("set up default route")
    def set_up_web_server(self):
        pass
    def set_up_some_service(self):
        pass
