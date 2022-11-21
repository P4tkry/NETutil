import ipaddress

import inquirer
from rich.table import Table
from rich.console import Console
from utils.object.host import Host
from utils.object.interfaces import Interface
from utils.object.mac_vendors import get_mac_vendor
from utils.scans.arp_scan import arp_scan
from utils.scans.icmp_scan import icmp_scan
from utils.scans.netbios_scan import netbios_scan


class Scan:
    def __init__(self, scan_type: str, console: Console, interface: Interface):
        self.type = scan_type
        self.console: Console = console
        self.interface: Interface = interface
        self.found_hosts: dict[ipaddress.IPv4Address, Host] = {}

    def start(self):
        if self.type == 'full':
            self.console.clear()
            arp_scan(console=self.console, ip_list=list(self.interface.network.hosts()), interface=self.interface,
                     found_hosts=self.found_hosts)
            netbios_scan(console=self.console, interface=self.interface,
                         found_hosts=self.found_hosts)
            icmp_scan(console=self.console, ip_list=list(self.interface.network.hosts()), interface=self.interface,
                      found_hosts=self.found_hosts)
            self.summary()

    def summary(self):
        iface_table = Table()

        iface_table.add_column("ip", justify="right", style="cyan", no_wrap=True)
        iface_table.add_column("mac", style="green")
        iface_table.add_column("netBIOS name", style="magenta")
        iface_table.add_column("TTL", style="magenta")
        iface_table.add_column("network card manufacturer", style="magenta")

        for host_ip in self.found_hosts:
            host_data = self.found_hosts[host_ip]
            mac_vendor = get_mac_vendor(host_data.mac)
            iface_table.add_row(str(host_data.ip), str(host_data.mac),
                                str(f'[deep_sky_blue4]{host_data.netbios_name}[/]'),
                                str(host_data.ttl), mac_vendor)
        self.console.print(iface_table)


class Scans:
    def __init__(self, console: Console):
        self.scans: dict[str, Scan] = {}
        self.console: Console =console

    def save(self, scan: Scan):
        questions = [
            inquirer.Confirm('save',
                             message="Do you want to save this scan?",
                             ),
        ]
        save = inquirer.prompt(questions)['save']
        if save:
            questions = [
                inquirer.Text('name',

                              message="Name this scan",
                              validate=lambda _, scan_name: False if scan_name in self.scans.keys() else True
                              ),

            ]

        name = inquirer.prompt(questions)['name']
        self.scans[name] = scan

    def select(self):
        if len(self.scans.keys()) == 0:
            self.console.print('[red]No scan list found[/]')
            return None

        questions = [
            inquirer.List('scan',
                          message="Select hosts list",
                          choices=self.scans.keys(),
                          ),
        ]
        return self.scans[inquirer.prompt(questions)['scan']]
