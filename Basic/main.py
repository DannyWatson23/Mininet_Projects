from mininet.net import Mininet
from lib.router import Router
from lib.switch import Switch
from lib.host import Host
from lib.device import Device
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import sys
def main():
    net = Mininet()
    a1 = Router('1', [{'interface': 'eth0', 'ip': '10.1.1.1', 'netmask': '255.255.255.0', 'ext':True}, {'interface': 'eth1', 'ip': '12.1.1.1', 'netmask': '255.255.255.0'}], net, '122.1.1.4')
    a2 = Router('2', [{'interface': 'eth0', 'ip': '10.1.1.2', 'netmask': '255.255.255.0', 'ext':True}, {'interface': 'eth1', 'ip': '13.1.1.1', 'netmask': '255.255.255.0'}], net, '122.1.2.4')
    s1 = Switch('1', [{'interface': 'eth0', 'ip': '0.0.0.0', 'netmask': '0.0.0.0', 'netw': '12.1.1.0'}, {'interface': 'eth1', 'ip': '0.0.0.0', 'netmask': '255.255.255.0'}], net, '122.1.1.5')
    s2 = Switch('2', [{'interface': 'eth0', 'ip': '0.0.0.0', 'netmask': '0.0.0.0', 'netw': '13.1.1.0'}, {'interface': 'eth1', 'ip': '0.0.0.0', 'netmask': '255.255.255.0'}], net, '122.1.2.5')
    h1 = Host('1', [{'interface': 'eth0', 'ip': '12.1.1.200', 'netmask': '255.255.255.0'}], net, '122.1.1.200')
    h2 = Host('2', [{'interface': 'eth0', 'ip': '13.1.1.200', 'netmask': '255.255.255.0'}], net, '122.1.2.200')
    a1.connect_devices(a1, a2, net, a1.ext_int, a2.ext_int)
    s1.connect_devices(s1, a1, net, s1.interfacelist[0]['eth0'],a1.interfacelist[0]['eth1'])
    s2.connect_devices(s2, a2, net, s2.interfacelist[0]['eth0'],a2.interfacelist[0]['eth1'])
    h1.connect_devices(h1, s1, net, h1.interfacelist[0]['eth0'],s1.interfacelist[0]['eth1'])
    h2.connect_devices(h2, s2, net, h2.interfacelist[0]['eth0'],s2.interfacelist[0]['eth1'])
    net.build()
    a1.initialise()
    a1.set_up_default_ext_route(a2.interfaces[0]['ip'])
    a2.initialise()
    a2.set_up_default_ext_route(a1.interfaces[0]['ip'])
    h1.initialise()
    h2.initialise()
    h1.set_up_route('ip r a default via '+a1.interfaces[1]['ip'])
    h2.set_up_route('ip r a default via '+a2.interfaces[1]['ip'])
    s1.initialise()
    s2.initialise()
    net.start()
    CLI(net)
    net.stop()



if __name__ == '__main__':
    setLogLevel('debug')
    main()
