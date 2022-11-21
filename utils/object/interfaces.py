from ipaddress import IPv4Address, IPv4Network

import inquirer
import psutil
from rich.console import Console
from rich.table import Table
from scapy.config import conf

from utils.object.mac_vendors import get_mac_vendor


class Interface:
    def __init__(self, name: str, mac: str, isup: bool, ip: IPv4Address, netmask: IPv4Address):
        self.name: str = name
        self.mac: str = mac.replace('-', ":")
        self.isup: bool = isup
        self.ip: IPv4Address = ip
        self.netmask: IPv4Address = netmask
        self.vendor: str | None = get_mac_vendor(mac)
        self.network: IPv4Network = IPv4Network(f'{ip}/{netmask}', strict=False)


class Interfaces:

    def __init__(self, console: Console):
        self.interfaces: dict[str, Interface] = {}
        self.console = console

    def fetch(self):
        interfaces_stats = psutil.net_if_stats()
        interfaces = psutil.net_if_addrs()

        for iface in interfaces:
            if iface in interfaces_stats and interfaces[iface][0].address and interfaces[iface][1].address and \
                    interfaces[iface][1].netmask:
                self.interfaces[iface] = Interface(mac=interfaces[iface][0].address,
                                                   ip=IPv4Address(interfaces[iface][1].address),
                                                   isup=interfaces_stats[iface].isup, name=iface,
                                                   netmask=IPv4Address(interfaces[iface][1].netmask))

    def present(self):
        iface_table = Table()

        iface_table.add_column("Interface", justify="right", style="cyan", no_wrap=True)
        iface_table.add_column("connected", style="green")
        iface_table.add_column("ip", style="magenta")
        iface_table.add_column("subnet mask", style="magenta")
        iface_table.add_column("mac address", style="magenta")
        iface_table.add_column("manufacturer", style="magenta")

        for iface in self.interfaces:
            iface_data = self.interfaces[iface]
            iface_table.add_row(iface,
                                f'{"[green]" if iface_data.isup else "[red]"}{str(iface_data.isup)}[/]',
                                str(iface_data.ip), str(iface_data.netmask),
                                str(iface_data.mac),
                                str(iface_data.vendor))
        self.console.print(iface_table)

        questions = [
            inquirer.List('interface',
                          message="What action do you want to do?",
                          choices=self.interfaces.keys(),
                          ),
        ]
        iface_name = inquirer.prompt(questions)['interface']

        return self.interfaces[iface_name]
