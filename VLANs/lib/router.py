from mininet.net import Mininet
from lib.device import Device
import time
from mininet.log import setLogLevel, info

class Router(Device):
    print("Created Router")
    def __init__(self, clusternum, interface_info, net_obj):
        self.clusternum = clusternum
        self.interface_info = interface_info
        self.net_obj = net_obj
        self.host = ''
        super().__init__(self.net_obj, self.clusternum, self.interface_info, 'router')
        self.host = self.net_obj.addHost(self.id)
        self.set_up_forwarding()
        self.set_up_ospf()
    def nat_ips(self):
        self.host.cmd('iptables -t nat -A POSTROUTING -o '+self.interfacelist[0]['eth0']+' -j SNAT --to '+self.interface_info[0]['ip'])
    def set_up_default_ext_route(self, adj_ip):
        self.host.cmd('ip r a default via '+adj_ip+' dev '+self.interfacelist[0]['eth0'])
    def set_up_forwarding(self):
        self.host.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    def set_up_ospf(self):
        self.host.cmd("echo 'hostname r"+self.clusternum+"\nlog file /var/log/quagga/r"+self.clusternum+".log\nrouter ospf\n ospf router-id "+self.loopback_ip+"\n  redistribute connected\n  redistribute static' > /etc/quagga/r"+self.clusternum+"ospfd.conf")
        self.host.cmd("echo 'hostname r"+self.clusternum+"\npassword en\nenable password en\ninterface lo\n  ip address "+self.loopback_ip+"/32\n\n' >> /etc/quagga/r"+self.clusternum+"zebra.conf")
        for i in self.interfaces:
            _ = i['ip'].split('.')
            print(_)
            network = _[0]+'.'+_[1]+'.'+_[2]+'.0/24'
            interface = 'r'+self.clusternum+'-'+i['interface']
            self.host.cmd("echo '\tnetwork "+network+" area 0\n' >> /etc/quagga/r"+self.clusternum+"ospfd.conf")
            self.host.cmd("echo 'interface "+interface+"\n '>> /etc/quagga/r"+self.clusternum+"zebra.conf")
            self.host.cmd("echo '\tnetwork "+network+"\n' >> /etc/quagga/r"+self.clusternum+"zebra.conf")
        time.sleep(0.1)
        self.host.cmd("zebra -f /etc/quagga/zebra.conf -d -z /tmp/r"+self.clusternum+"zeb.sock -i /tmp/r"+self.clusternum+"zeb.pid")
        time.sleep(0.1)
        self.host.cmd("ospfd -f /etc/quagga/r"+self.clusternum+"ospfd.conf -d -z /tmp/r"+self.clusternum+"zeb.sock -i /tmp/r"+self.clusternum+"ospfd.pid")
    def enable_8021q(self):
        self.host.cmd("sudo modprobe 8021q")
