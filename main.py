import ipaddress
from rich.console import Console
from rich.progress import Progress, track
import time
from client import Client
import psutil
import inquirer
import logging
from interactions.select_interface import select_interface
from utils.scans import Scan
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
client = Client()
console = Console()

def welcome():
    console.print('''
[red1]
    _   ______________[dodger_blue2]      __  _ __[/]
   / | / / ____/_  __/[dodger_blue2]_  __/ /_(_) /[/]
  /  |/ / __/   / / [dodger_blue2]/ / / / __/ / / [/]
 / /|  / /___  / / [dodger_blue2]/ /_/ / /_/ / /  [/]
/_/ |_/_____/ /_/  [dodger_blue2]\__,_/\__/_/_/   [/][/]
                        [red]by [link=https://github.com/P4tkry]P4tkry[/link][/]\n''')


def menu():
    questions = [
        inquirer.List('action',
                      message="What action do you want to do?",
                      choices=['scan', 'attack'],
                      ),
    ]
    action = inquirer.prompt(questions)['action']

    if action == 'scan':
        console.clear()
        interface = select_interface(client=client, console=console)
        print(interface)
        scan = Scan(scan_type='full', console=console, interface=interface,
                    network=ipaddress.ip_network(
                        f'{interface["ip"]}/{interface["netmask"]}',
                        strict=False))
        scan.start()


def main():
    welcome()
    menu()


main()
