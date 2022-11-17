from client import Client
from rich.console import Console
from rich.table import Table
import inquirer


def select_interface(client: Client, console: Console):
    iface_table = Table()

    iface_table.add_column("Interface", justify="right", style="cyan", no_wrap=True)
    iface_table.add_column("connected", style="green")
    iface_table.add_column("ip", style="magenta")
    iface_table.add_column("subnet mask", style="magenta")
    iface_table.add_column("mac address", style="magenta")
    iface_table.add_column("manufacturer", style="magenta")

    for iface in client.interfaces:

        iface_data = client.interfaces[iface]
        iface_table.add_row(iface,
                            f'{"[green]" if iface_data["isup"] else "[red]"}{str(iface_data["isup"])}[/]',
                            str(iface_data['ip']), str(iface_data['netmask']),
                            str(iface_data['mac']),
                            str(iface_data['vendorName']))
    console.print(iface_table)

    questions = [
        inquirer.List('interface',
                      message="What action do you want to do?",
                      choices=client.interfaces.keys(),
                      ),
    ]
    iface_name= inquirer.prompt(questions)['interface']

    return client.interfaces[iface_name]
