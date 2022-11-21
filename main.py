import ipaddress
from rich.console import Console
from rich.progress import Progress, track
import time
import psutil
import inquirer

from utils.attacks import Attack
import logging

from utils.object.interfaces import Interfaces
from utils.scans import Scan, Scans

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


class NETutil:
    def __init__(self):
        self.console = Console()
        self.scans: Scans = Scans(console=self.console)
        self.interfaces = Interfaces(console=self.console)
        self.interfaces.fetch()
        self.welcome()
        self.menu()

    def welcome(self):
        self.console.print('''
    [red1]
        _   ______________[dodger_blue2]      __  _ __[/]
       / | / / ____/_  __/[dodger_blue2]_  __/ /_(_) /[/]
      /  |/ / __/   / / [dodger_blue2]/ / / / __/ / / [/]
     / /|  / /___  / / [dodger_blue2]/ /_/ / /_/ / /  [/]
    /_/ |_/_____/ /_/  [dodger_blue2]\__,_/\__/_/_/   [/][/]
                            [red]by [link=https://github.com/P4tkry]P4tkry[/link][/]\n''')

    def menu(self):
        self.console.clear()
        self.console.rule('[dodger_blue2]MENU[/]')
        questions = [
            inquirer.List('action',
                          message="What action do you want to do?",
                          choices=['scan', 'attack'],
                          ),
        ]
        action = inquirer.prompt(questions)['action']

        if action == 'scan':
            self.console.clear()
            interface = self.interfaces.present()
            scan = Scan(scan_type='full', console=self.console, interface=interface)
            scan.start()
            self.scans.save(scan)

        if action == 'attack':
            attack = Attack(scans=self.scans, console=self.console)
            attack.select_victims()
            attack.start()

        return self.menu()


NETutil()
