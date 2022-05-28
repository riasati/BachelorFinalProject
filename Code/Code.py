import subprocess
from time import sleep

from mininet.net import Mininet
from mininet.node import Host, Switch
# from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.topo import Topo

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
            interface, _ = host.connectionsTo(switch)[0]
            interface.setIP('10.0.{}.{}/24'.format(switch_i, host_i))

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
    def build(self, Adelay, Bdelay):
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

        self.addLink(s1, s2, bw=10, delay=Adelay) #  delay='5ms'
        self.addLink(s3, s4, bw=20, delay=Bdelay)


if '__main__' == __name__:
    setLogLevel('info')
    net = Mininet(topo=MPTopo(Adelay="20ms",Bdelay="20ms"), link=TCLink)
    write_sysctl('net.mptcp.mptcp_enabled', 1)

    setup_mptcp(net)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')

    # result = h1.cmd('iperf h2')
    # print(result)
    # net.iperf((h1, h2))

    print("Starting test...")
    # h1.cmd('while true; do iperf h2; sleep 1; &') # done > /tmp/iperfh1h2.out
    h2.cmd('iperf -s &')
    # h1.cmd('iperf', '-c', h2.IP() , '-t', '10')
    h1.cmd('iperf -c ' + h2.IP() + " -t 50 > result &")
    # h2.cmdPrint('iperf -c 10.0.1.1 -i 1')
    # net.iperf((h1, h2))
    sleep(10)
    # h3.cmd('while true; do iperf h4; sleep 1; &')
    h4.cmd('iperf -s &')
    # h1.cmd('iperf', '-c', h2.IP() , '-t', '10')
    h3.cmd('iperf -c ' + h4.IP() + " -t 20 > result &")
    # net.iperf((h3, h4))
    # sleep(20)
    # h3.cmd('kill %while')
    # sleep(20)
    sleep(40)
    # h1.cmd('kill %while')
    print("Stopping test")
    # print("Reading output")
    # f = open('/tmp/iperfh1h2.out')
    # lineno = 1
    # for line in f.readlines():
    #     print("%d: %s" % (lineno, line.strip()))
    #     lineno += 1
    # f.close()

    # print("Starting test...")
    # h3.cmd('while true; do iperf h4; sleep 1; done > /tmp/iperfh3h4.out &')
    # sleep(10)
    # print("Stopping test")
    # h3.cmd('kill %while')
    # print("Reading output")
    # f = open('/tmp/iperfh1h2.out')
    # lineno = 1
    # for line in f.readlines():
    #     print("%d: %s" % (lineno, line.strip()))
    #     lineno += 1
    # f.close()

    # We need to give mptcp some time
    # print('=========================================================')
    # print('Set up two paths with 5 MBit each. Running iperf in 3s...')
    # print('=========================================================')
    # sleep(3)
    # CLI(net)
    # h1, h2, h3, h4 = [net.get(n) for n in hostnames]
    # h1.cmd('iperf -s &')
    # h2.cmdPrint('iperf -c 10.0.1.1 -i 1')
    net.stop()