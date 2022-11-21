import threading
from ipaddress import IPv4Address

from rich.console import Console
from rich.progress import Progress
from scapy.layers.inet import UDP, IP, ICMP
from scapy.layers.l2 import Ether, ARP

from scapy.sendrecv import srp1, sr1
from utils.object.host import Host
from utils.object.interfaces import Interface


def icmp_scan(console: Console, interface: Interface, ip_list: list[IPv4Address],
              found_hosts: dict[IPv4Address, Host]):
    def _icmp_scan_thread_(host_ip: IPv4Address, update_progress):
        response = srp1(Ether(src=interface.mac) / IP(dst=str(host_ip)) / ICMP(), iface=interface.name, timeout=5, verbose=0)
        if response:
            if not found_hosts[host_ip]:
                found_hosts[host_ip] = Host(ip=host_ip, mac=response.hwsrc)
            found_hosts[host_ip].ttl = response.ttl
        update_progress()

    console.rule('[bright_magenta]ICMP scan[/]')
    with Progress() as progress:
        scan = progress.add_task("[yellow]Scanning ICMP hosts[/]", total=len(ip_list))
        threads = []
        for ip in found_hosts:
            threads.append(threading.Thread(target=_icmp_scan_thread_,
                                            args=(ip, lambda: progress.update(scan, advance=1))))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        progress.remove_task(scan)
