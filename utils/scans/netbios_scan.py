import threading
from ipaddress import IPv4Address

from rich.console import Console
from rich.progress import Progress
from scapy.layers.inet import UDP, IP
from scapy.layers.netbios import NBNSQueryRequest
from scapy.packet import Raw
from scapy.sendrecv import srp1, sr1
from rich import print
from utils.object.host import Host
from utils.object.interfaces import Interface


def netbios_scan(console: Console, interface: Interface, found_hosts: dict[IPv4Address, Host]):
    def _netbios_scan_thread_(host_ip: IPv4Address, update_progress):
        response = sr1(IP(dst=str(host_ip)) / UDP(sport=137) / NBNSQueryRequest(NAME_TRN_ID=0x8228,
                                                                                QUESTION_NAME='*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                                                                                QUESTION_TYPE='NBSTAT', FLAGS=0x0000),
                       iface=interface.name, timeout=5, verbose=0)
        if response:
            try:
                data = bytes(response[Raw].load)
                found_hosts[host_ip].netbios_name = data[25:41].decode()
                print(f'[deep_sky_blue4][✓] found netBIOS name for {host_ip} : [green]{data[25:41].decode()}[/][/]')
            except:
                pass
        update_progress()

    console.rule('[deep_sky_blue4]netBIOS name scan[/]')
    with Progress() as progress:
        scan = progress.add_task("[yellow]Scanning netBIOS names[/]", total=len(found_hosts))
        threads = []
        for ip in found_hosts:
            threads.append(threading.Thread(target=_netbios_scan_thread_,
                                            args=(ip, lambda: progress.update(scan, advance=1))))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        progress.remove_task(scan)
