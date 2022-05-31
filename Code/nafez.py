import os
import time
import threading
import subprocess
from mininet.net import Mininet
from time import sleep
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import Host, Switch
from mininet.log import setLogLevel
from mininet.topo import Topo

file = open('final_result_1.txt', 'a')
#file.truncate(0)
def write_sysctl(key, value):
    """ Write kernel parameters. """
    subprocess.check_output('sysctl -w {}={}'.format(key, value), shell=True)

def setup_mptcp(net):
    hosts = [v for v in net.values() if isinstance(v, Host)]
    switches = [v for v in net.values() if isinstance(v, Switch)]
    for switch_i, switch in enumerate(switches, start=1):
        for host_i, host in enumerate(hosts, start=1):
            # connectionsTo returns list of (host-interface, switch-interface)
            # we want the host interface connected to the switch
            tmp = host.connectionsTo(switch)
	    if len(tmp)>0:
	    	interface, _ = tmp[0]
            	interface.setIP('10.0.{}.{}/24'.format(switch_i, host_i))


net = Mininet(link=TCLink)
h1 = net.addHost( 'h1' )
h2 = net.addHost( 'h2' )
h3 = net.addHost( 'h3' )
h4 = net.addHost( 'h4' )
s1 = net.addSwitch( 's1' )
s2 = net.addSwitch( 's2' )
s3 = net.addSwitch( 's3' )
s4 = net.addSwitch( 's4' )
c0 = net.addController( 'c0')

l1 = net.addLink( h1, s1, bw=100, delay=100)
l2 = net.addLink( h1, s3, bw=100 ,delay=100)
l3 = net.addLink( h3, s3, bw=100, delay=100)
l4 = net.addLink( h2, s2, bw=100, delay=100)
l5 = net.addLink( h2, s4, bw=100, delay=100)
l6 = net.addLink( h4, s4, bw=100, delay=100)

A = net.addLink( s1, s2, bw=10, delay=20)
B = net.addLink( s3, s4, bw=20, delay=20)

setLogLevel('info')
write_sysctl('net.mptcp.mptcp_enabled', 1)
os.system('modprobe mptcp_olia && sysctl -w net.ipv4.tcp_congestion_control=OLIA')
setup_mptcp(net)
net.start()

print('=========================================================')
print('Set up two paths with 5 MBit each. Running iperf in 3s...')
print('=========================================================')
sleep(3)

print(h2.cmd('iperf -s &'))
print(h4.cmd('iperf -s &'))


def mptcp_conn():
    str=h1.cmd('iperf -c', h2.IP(), '-t 50')
    file.write(str)
print(str)
def tcp_conn():
    time.sleep(10.0)
    print(h3.cmd('iperf -c', h4.IP(), '-Z cubic -t 20'))

for nn in range(20):
    for d in [20, 40, 60, 80, 100]:
        B.delay=d
        t1 = threading.Thread(target=mptcp_conn, args=())
        t2 = threading.Thread(target=tcp_conn, args=())

        t1.start()
        t2.start()

        t1.join()
        t2.join()
    print('n th: ', nn)
f.close()
print("Done!")
net.stop()



