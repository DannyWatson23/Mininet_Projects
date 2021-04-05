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
    a1 = Router('1', [{'interface': 'eth0', 'ip': '10.1.1.1', 'netmask': '255.255.255.0', 'ext':True},{'interface': 'eth1', 'ip': '12.1.1.1', 'netmask': '255.255.255.0'}, {'interface': 'eth2', 'ip':'20.1.1.2', 'netmask': '255.255.255.252'},{'interface': 'lo', 'ip': '122.1.1.4'}], net)
    a2 = Router('2', [{'interface': 'eth0', 'ip': '10.1.1.2', 'netmask': '255.255.255.0', 'ext':True}, {'interface': 'eth1', 'ip': '13.1.1.1', 'netmask': '255.255.255.0'}, {'interface': 'eth2', 'ip':'20.1.2.2', 'netmask': '255.255.255.252'},{'interface': 'lo', 'ip': '122.1.2.4'}], net)
    a3 = Router('3', [{'interface': 'eth0', 'ip': '20.1.1.1', 'netmask': '255.255.255.252'},{'interface': 'eth1', 'ip': '20.1.2.1', 'netmask': '255.255.255.252'}, {'interface': 'lo', 'ip': '122.1.3.4'}], net)
    s1 = Switch('1', [{'interface': 'eth0', 'ip': '12.1.1.10', 'netmask': '255.255.255.0', 'netw': a1.interfaces[0]['ip']},{'interface': 'eth1'},{'interface': 'eth2'}, {'interface': 'eth3'}, {'interface': 'lo', 'ip':'122.1.1.5'}, ], net)
    s2 = Switch('2', [{'interface': 'eth0', 'ip': '13.1.1.10', 'netmask': '255.255.255.0', 'netw':  a2.interfaces[0]['ip']}, {'interface': 'lo', 'ip': '122.1.2.5'},{'interface': 'eth1'}], net)
    h1 = Host('1', [{'interface': 'eth0', 'ip': '12.1.1.200', 'netmask': '255.255.255.0'}, {'interface': 'lo', 'ip': '122.1.1.200'}], net)
    h2 = Host('2', [{'interface': 'eth0', 'ip': '13.1.1.200', 'netmask': '255.255.255.0'}, {'interface': 'lo', 'ip': '122.1.2.200'}], net)
    h3 = Host('1', [{'interface': 'eth0', 'ip': '12.1.1.201', 'netmask': '255.255.255.0'}, {'interface': 'lo', 'ip':'122.1.1.201'}], net)
    h4 = Host('1', [{'interface': 'eth0', 'ip': '12.1.1.202', 'netmask': '255.255.255.0'}, {'interface': 'lo', 'ip':'122.1.1.202'}], net)
    a1.connect_devices(a1, a2, net, a1.interfacelist[0]['eth0'], a2.interfacelist[0]['eth0'])
    a3.connect_devices(a3, a1, net, a3.interfacelist[0]['eth0'], a1.interfacelist[0]['eth2'])
    a3.connect_devices(a3, a2, net, a3.interfacelist[0]['eth1'], a2.interfacelist[0]['eth2'])
    s1.connect_devices(s1, a1, net, s1.interfacelist[0]['eth0'],a1.interfacelist[0]['eth1'])
    s2.connect_devices(s2, a2, net, s2.interfacelist[0]['eth0'],a2.interfacelist[0]['eth1'])
    h1.connect_devices(h1, s1, net, h1.interfacelist[0]['eth0'],s1.interfacelist[0]['eth1'])
    h2.connect_devices(h2, s2, net, h2.interfacelist[0]['eth0'],s2.interfacelist[0]['eth1'])
    h3.connect_devices(h3, s1, net, h3.interfacelist[0]['eth0'],s1.interfacelist[0]['eth2'])
    h4.connect_devices(h4, s1, net, h4.interfacelist[0]['eth0'], s1.interfacelist[0]['eth3'])
    net.build()
    a1.initialise(a1.host)
    a2.initialise(a2.host)
    a3.initialise(a3.host)
    h1.initialise(h1.host)
    h2.initialise(h2.host)
    h3.initialise(h3.host)
    h4.initialise(h4.host)
    a1.nat_ips()
    a2.nat_ips()
    h1.set_up_route('ip r a default via '+a1.interfaces[1]['ip'], h1.host)
    h2.set_up_route('ip r a default via '+a2.interfaces[1]['ip'], h2.host)
    h3.set_up_route('ip r a default via '+a1.interfaces[1]['ip'], h3.host)
    h4.set_up_route('ip r a default via '+a1.interfaces[1]['ip'], h4.host)
    s1.initialise(s1.host)
    s2.initialise(s2.host)
    net.start()
    net.startTerms()
    cli = CLI(net)
    CLI.do_xterm(cli, "r1 sw1 h1")
    net.stop()



if __name__ == '__main__':
    #setLogLevel('info')
    main()
