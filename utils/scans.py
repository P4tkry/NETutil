import ipaddress
import time

import psutil
import scapy
from psutil._common import snicaddr
from rich.progress import Progress
from scapy import *
from scapy.layers.inet import ICMP, IP
import inquirer
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import sr1, sr, srp, srp1
import nmap
from client import Client
from rich import print
from rich.console import Console
from rich.table import Table
import threading
from interactions.select_interface import select_interface


class Scan:
    def __init__(self, scan_type: str, console: Console, interface: select_interface, network: ipaddress.IPv4Network):
        self.type = scan_type
        self.console = console
        self.interface = interface
        self.network = network
        self.found_hosts={}

    def start(self):
        if self.type == 'full':
            self.console.clear()
            self._arp_scan_()

    def _arp_scan_thread_(self, ip: str, update_progress):
        packet = Ether(src=self.interface['mac'].lower()) / ARP(pdst=ip, psrc=self.interface["ip"])
        resp = srp1(packet, timeout=5, verbose=0)
        if resp:
            self.found_hosts[ip]=resp.hwsrc
            print(f'[green][✓] found host {ip}[/]')
        update_progress()

    def _arp_scan_(self):

        with Progress() as progress:
            scan = progress.add_task("[yellow]Scanning devices[/]", total=self.network.num_addresses)
            threads = []
            for ip in [str(ip) for ip in self.network]:
                threads.append(threading.Thread(target=self._arp_scan_thread_, args=(ip, lambda: progress.update(scan, advance=1))))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            progress.remove_task(scan)


# def _ping_scan_(self):
#     for ip in self.ip_addresses:
#         ping_response = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0)
#         if ping_response:
#             self.console.print(f'[green][✓] host {ip} responded for ICMP request[/]')
