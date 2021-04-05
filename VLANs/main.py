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
    a1 = Router('1', [{'interface': 'eth0', 'ip': '12.1.1.1', 'netmask': '255.255.255.0'}, {'interface': 'eth2', 'ip':'20.1.1.2', 'netmask': '255.255.255.252'},{'interface': 'lo', 'ip': '122.1.1.4'}], net)
    s1 = Switch('1', [{'interface': 'eth0', 'ip': '12.1.1.10', 'netmask': '255.255.255.0', 'netw': a1.interfaces[0]['ip']},{'interface': 'eth1'},{'interface': 'eth2'}, {'interface': 'eth3'}, {'interface': 'lo', 'ip':'122.1.1.5'}, ], net)
    h1 = Host('1', [{'interface': 'eth0', 'ip': '12.1.1.200', 'netmask': '255.255.255.0'}, {'interface': 'lo', 'ip': '122.1.1.200'}], net)
    h3 = Host('1', [{'interface': 'eth0', 'ip': '12.2.1.200', 'netmask': '255.255.255.0'}, {'interface': 'lo', 'ip':'122.1.1.201'}], net)
    s1.connect_devices(s1, a1, net, s1.interfacelist[0]['eth0'],a1.interfacelist[0]['eth0'])
    h1.connect_devices(h1, s1, net, h1.interfacelist[0]['eth0'],s1.interfacelist[0]['eth1'])
    h3.connect_devices(h3, s1, net, h3.interfacelist[0]['eth0'],s1.interfacelist[0]['eth2'])
    net.build()
    a1.initialise(a1.host)
    h1.initialise(h1.host)
    h3.initialise(h3.host)
    h1.set_up_route('ip r a default via '+a1.interfaces[1]['ip'], h1.host)
    h3.set_up_route('ip r a default via '+a1.interfaces[1]['ip'], h3.host)
    s1.initialise(s1.host)
    a1.execute('ifconfig r1-eth0 0.0.0.0')
    a1.execute('vconfig add r1-eth0 100')
    a1.execute('vconfig add r1-eth0 200')
    a1.execute('ifconfig r1-eth0.100 12.1.1.1 netmask 255.255.255.0 up')
    a1.execute('ifconfig r1-eth0.200 12.2.1.1 netmask 255.255.255.0 up')
    s1.execute('ifconfig sw1-eth0 up 0.0.0.0 ')
    s1.execute('ifconfig sw1-eth1 up 0.0.0.0')
    s1.execute('brctl delbr br0')
    s1.execute('brctl addbr br100')
    s1.execute('brctl addbr br200')
    s1.execute('ip link add link sw1-eth0 name sw1-eth0.100 type vlan id 100')
    s1.execute('ip link add link sw1-eth0 name sw1-eth0.200 type vlan id 200')
    s1.execute('ip link add link sw1-eth1 name sw1-eth1.100 type vlan id 100')
    s1.execute('ip link add link sw1-eth2 name sw1-eth2.200 type vlan id 200')
    s1.execute('ifconfig sw1-eth0.100 up')
    s1.execute('ifconfig sw1-eth1.100 up')
    s1.execute('ifconfig sw1-eth2.200 up')
    s1.execute('ifconfig sw1-eth0.200 up')
    s1.execute('ifconfig br100 12.1.1.10 netmask 255.255.255.0 up')
    s1.execute('ifconfig br200 12.2.1.10 netmask 255.255.255.0 up')
    s1.execute('brctl addif br100 sw1-eth0.100 sw1-eth1.100 sw1-eth0 sw1-eth1')
    s1.execute('brctl addif br200 sw1-eth0.200 sw1-eth2.200 sw1-eth0 sw1-eth2')
    s1.execute('sysctl -w net.bridge.bridge-nf-filter-vlan-tagged=1')
    s1.execute('sysctl -w net.ipv4.ip_forward=1')
    net.start()
    CLI(net)
    net.stop()



if __name__ == '__main__':
    setLogLevel('info')
    main()
