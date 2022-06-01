import os
import threading
import subprocess
from time import sleep
from optparse import OptionParser
from mininet.net import Mininet
from mininet.node import Host, Switch
# from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.topo import Topo


# def setup_mptcp(net):
#     hosts = [v for v in net.values() if isinstance(v, Host)]
#     switches = [v for v in net.values() if isinstance(v, Switch)]
#     for switch_i, switch in enumerate(switches, start=1):
#         for host_i, host in enumerate(hosts, start=1):
#             # connectionsTo returns list of (host-interface, switch-interface)
#             # we want the host interface connected to the switch
#             interface, _ = host.connectionsTo(switch)[0]
#             interface.setIP('10.0.{}.{}/24'.format(switch_i, host_i))

# mode 1 : congestionControl = lia, pathManager = default
# mode 2 : congestionControl = olia, pathManager = default
# mode 3 : congestionControl = wvegas, pathManager = default
# mode 4 : congestionControl = balia, pathManager = default
# mode 5 : congestionControl = lia, pathManager = fullmesh
# mode 6 : congestionControl = olia, pathManager = fullmesh
# mode 7 : congestionControl = wvegas, pathManager = fullmesh
# mode 8 : congestionControl = balia, pathManager = fullmesh
# mode 9 : congestionControl = lia, pathManager = ndiffports
# mode 10 : congestionControl = olia, pathManager = ndiffports
# mode 11 : congestionControl = wvegas, pathManager = ndiffports
# mode 12 : congestionControl = balia, pathManager = ndiffports
# mode 13 : congestionControl = lia, pathManager = binder
# mode 14 : congestionControl = olia, pathManager = binder
# mode 15 : congestionControl = wvegas, pathManager = binder
# mode 16 : congestionControl = balia, pathManager = binder
def setupCongestionControll(mode=1):
    subprocess.check_output('sudo sysctl -w {}={}'.format("net.mptcp.mptcp_enabled", 1), shell=True)
    if mode == 1:
        os.system('sudo modprobe mptcp_coupled && sudo sysctl -w net.ipv4.tcp_congestion_control=lia ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=default ')
    elif mode == 2:
        os.system('sudo modprobe mptcp_olia && sudo sysctl -w net.ipv4.tcp_congestion_control=olia ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=default ')
    elif mode == 3:
        os.system('sudo modprobe mptcp_wvegas && sudo sysctl -w net.ipv4.tcp_congestion_control=wvegas ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=default ')
    elif mode == 4:
        os.system('sudo modprobe mptcp_balia && sudo sysctl -w net.ipv4.tcp_congestion_control=balia ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=default ')
    elif mode == 5:
        os.system('sudo modprobe mptcp_coupled && sudo sysctl -w net.ipv4.tcp_congestion_control=lia ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=fullmesh ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_fullmesh/parameters/num_subflows')
    elif mode == 6:
        os.system('sudo modprobe mptcp_olia && sudo sysctl -w net.ipv4.tcp_congestion_control=olia ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=fullmesh ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_fullmesh/parameters/num_subflows')
    elif mode == 7:
        os.system('sudo modprobe mptcp_wvegas && sudo sysctl -w net.ipv4.tcp_congestion_control=wvegas ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=fullmesh ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_fullmesh/parameters/num_subflows')
    elif mode == 8:
        os.system('sudo modprobe mptcp_balia && sudo sysctl -w net.ipv4.tcp_congestion_control=balia ')
        os.system('sudo sysctl -w net.mptcp.mptcp_path_manager=fullmesh ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_fullmesh/parameters/num_subflows')
    elif mode == 9:
        os.system('sudo modprobe mptcp_coupled && sudo sysctl -w net.ipv4.tcp_congestion_control=lia ')
        os.system('sudo modprobe mptcp_ndiffports && sudo sysctl -w net.mptcp.mptcp_path_manager=ndiffports ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows')
    elif mode == 10:
        os.system('sudo modprobe mptcp_olia && sudo sysctl -w net.ipv4.tcp_congestion_control=olia ')
        os.system('sudo modprobe mptcp_ndiffports && sudo sysctl -w net.mptcp.mptcp_path_manager=ndiffports ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows')
    elif mode == 11:
        os.system('sudo modprobe mptcp_wvegas && sudo sysctl -w net.ipv4.tcp_congestion_control=wvegas ')
        os.system('sudo modprobe mptcp_ndiffports && sudo sysctl -w net.mptcp.mptcp_path_manager=ndiffports ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows')
    elif mode == 12:
        os.system('sudo modprobe mptcp_balia && sudo sysctl -w net.ipv4.tcp_congestion_control=balia ')
        os.system('sudo modprobe mptcp_ndiffports && sudo sysctl -w net.mptcp.mptcp_path_manager=ndiffports ')
        os.system('echo 1 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows')
    elif mode == 13:
        os.system('sudo modprobe mptcp_coupled && sudo sysctl -w net.ipv4.tcp_congestion_control=lia ')
        os.system('sudo modprobe mptcp_binder && sudo sysctl -w net.mptcp.mptcp_path_manager=binder ')
    elif mode == 14:
        os.system('sudo modprobe mptcp_olia && sudo sysctl -w net.ipv4.tcp_congestion_control=olia ')
        os.system('sudo modprobe mptcp_binder && sudo sysctl -w net.mptcp.mptcp_path_manager=binder ')
    elif mode == 15:
        os.system('sudo modprobe mptcp_wvegas && sudo sysctl -w net.ipv4.tcp_congestion_control=wvegas ')
        os.system('sudo modprobe mptcp_binder && sudo sysctl -w net.mptcp.mptcp_path_manager=binder ')
    elif mode == 16:
        os.system('sudo modprobe mptcp_balia && sudo sysctl -w net.ipv4.tcp_congestion_control=balia ')
        os.system('sudo modprobe mptcp_binder && sudo sysctl -w net.mptcp.mptcp_path_manager=binder ')

### CONFIGURATIONS ###

#sysctl net.mptcp
#sysctl net | grep congestion
#sysctl net | grep 'mptcp\|congestion'

# "congestion controls:"

#os.system('sysctl -w net.ipv4.tcp_congestion_control=cubic ')
#os.system('modprobe mptcp_coupled && sysctl -w net.ipv4.tcp_congestion_control=lia ')
#os.system('modprobe mptcp_olia && sysctl -w net.ipv4.tcp_congestion_control=olia ')
#os.system('modprobe mptcp_wvegas && sysctl -w net.ipv4.tcp_congestion_control=wvegas ')
#os.system('modprobe mptcp_balia && sysctl -w net.ipv4.tcp_congestion_control=balia ')

# "path-managers:"

#os.system('sysctl -w net.mptcp.mptcp_path_manager=default ')
# os.system('sysctl -w net.mptcp.mptcp_path_manager=fullmesh ')
# os.system('echo 1 | sudo tee /sys/module/mptcp_fullmesh/parameters/num_subflows')
#os.system('modprobe mptcp_ndiffports && sysctl -w net.mptcp.mptcp_path_manager=ndiffports ')
#os.system('echo 1 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows')
# os.system('modprobe mptcp_binder && sysctl -w net.mptcp.mptcp_path_manager=binder ')

# "scheduler:"

#os.system('sysctl -w net.mptcp.mptcp_scheduler=default ')
#os.system('modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin ')
#os.system('echo 1 | sudo tee /sys/module/mptcp_rr/parameters/num_segments')
#os.system('echo Y | sudo tee /sys/module/mptcp_rr/parameters/cwnd_limited')
#os.system('modprobe mptcp_redundant && sysctl -w net.mptcp.mptcp_scheduler=redundant ')

class MPTopo(Topo):
    # def build(self, hostnames, number_of_paths=2, bw=5):
    #     linkopt = dict(bw=bw)
    #
    #     for h in hostnames:
    #         self.addHost(h)
    #
    #     for i_p in range(0, number_of_paths):
    #         s = self.addSwitch('s{}'.format(i_p))
    #         for h in self.hosts():
    #             self.addLink(h, s, **linkopt)
    def __init__(self, Adelay, Bdelay):
        Topo.__init__(self)
        self.Adelay = Adelay
        self.Bdelay = Bdelay

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        hostSwitchLinkSpec = dict(bw=100, delay='0.1ms')
        # (or you can use brace syntax: linkopts = {'bw':10, 'delay':'5ms', ... } )
        self.addLink(h1, s1, **hostSwitchLinkSpec)
        self.addLink(h1, s3, **hostSwitchLinkSpec)
        self.addLink(h2, s2, **hostSwitchLinkSpec)
        self.addLink(h2, s4, **hostSwitchLinkSpec)
        self.addLink(h3, s3, **hostSwitchLinkSpec)
        self.addLink(h4, s4, **hostSwitchLinkSpec)

        self.addLink(s1, s2, bw=10, delay=self.Adelay)  # delay='5ms'
        self.addLink(s3, s4, bw=20, delay=self.Bdelay)

    # def build(self):
    #     h1 = self.addHost('h1')
    #     h2 = self.addHost('h2')
    #     h3 = self.addHost('h3')
    #     h4 = self.addHost('h4')
    #
    #     s1 = self.addSwitch('s1')
    #     s2 = self.addSwitch('s2')
    #     s3 = self.addSwitch('s3')
    #     s4 = self.addSwitch('s4')
    #
    #     hostSwitchLinkSpec = dict(bw=100, delay='0.1ms')
    #     # (or you can use brace syntax: linkopts = {'bw':10, 'delay':'5ms', ... } )
    #     self.addLink(h1, s1, **hostSwitchLinkSpec)
    #     self.addLink(h1, s3, **hostSwitchLinkSpec)
    #     self.addLink(h2, s2, **hostSwitchLinkSpec)
    #     self.addLink(h2, s4, **hostSwitchLinkSpec)
    #     self.addLink(h3, s3, **hostSwitchLinkSpec)
    #     self.addLink(h4, s4, **hostSwitchLinkSpec)
    #
    #     self.addLink(s1, s2, bw=10, delay=self.Adelay) #  delay='5ms'
    #     self.addLink(s3, s4, bw=20, delay=self.Bdelay)

def mptcpConnection(h1,h2,file):
    h1String = h1.cmd('iperf -c ' + h2.IP() + " -t 50 ")
    print(h1String)
    file.write(h1String)
    # str=h1.cmd('iperf -c', h2.IP(), '-t 50')
    # file.write(str)
def tcpConnection(h3,h4,file):
    time.sleep(10.0)
    h3String = h3.cmd('iperf -c ' + h4.IP() + " -t 20 ")
    print(h3String)
    file.write(h3String)
    # print(h3.cmd('iperf -c', h4.IP(), '-Z cubic -t 20'))

if '__main__' == __name__:
    parser = OptionParser()
    parser.add_option("--bdelay", dest="bdelay", default="20ms")
    parser.add_option("--mode", dest="mode", default=1)
    (options, args) = parser.parse_args()

    h2file = open('resultH2-' + options.bdelay + '-mode' + options.mode + '.txt', 'w')
    h4file = open('resultH4-' + options.bdelay + '-mode' + options.mode + '.txt', 'w')


    for i in range(20): #20
        print("Starting test number :" + str(i+1))
        setLogLevel('info')
        net = Mininet(topo=MPTopo(Adelay="20ms",Bdelay=options.bdelay), link=TCLink)
        setupCongestionControll(int(options.mode))
        net.start()
        h1 = net.get('h1')
        h2 = net.get('h2')
        h3 = net.get('h3')
        h4 = net.get('h4')
        sleep(3)
        print(h2.cmd('iperf -s &'))
        print(h4.cmd('iperf -s &'))

        # h1String = h1.cmd('iperf -c ' + h2.IP() + " -t 50 &")
        # print(h1String)
        # h2file.write(h1String)
        # sleep(10)
        #
        # print(h3.cmd('iperf -c ' + h4.IP() + " -t 20 > result2 &"))
        # sleep(40)
        t1 = threading.Thread(target=mptcpConnection, args=(h1,h2,h2file))
        t2 = threading.Thread(target=tcpConnection, args=(h3,h4,h4file))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        h2.cmd('kill %while')
        h4.cmd('kill %while')
        print("Stopping test number:" + str(i+1))
        net.stop()