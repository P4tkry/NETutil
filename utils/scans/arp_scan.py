import threading
from ipaddress import IPv4Address

from rich.console import Console
from rich.progress import Progress
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp1
from rich import print
from utils.object.host import Host
from utils.object.interfaces import Interface


def arp_scan(console: Console, interface: Interface, ip_list: list[IPv4Address],
             found_hosts: dict[IPv4Address, Host]):
    def _arp_scan_thread_(host_ip: IPv4Address, update_progress):
        response = srp1(Ether(src=interface.mac) / ARP(pdst=str(host_ip), psrc=str(interface.ip)), timeout=5,
                        verbose=0, iface=interface.name)
        if response:
            found_hosts[host_ip] = Host(ip=host_ip, mac=response.hwsrc)
            print(f'[green][✓] found host {host_ip}[/]')
        update_progress()

    console.rule('[yellow]ARP hosts scan[/]')
    with Progress() as progress:
        scan = progress.add_task("[yellow]Scanning devices[/]", total=len(ip_list))
        threads = []
        for ip in ip_list:
            threads.append(threading.Thread(target=_arp_scan_thread_,
                                            args=(ip, lambda: progress.update(scan, advance=1))))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        progress.remove_task(scan)
