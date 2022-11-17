import psutil
import json


class Client:
    def __init__(self):
        vendors_file = open('./data/mac-vendors.json', encoding="utf8")
        self.mac_vendors = json.load(vendors_file)
        vendors_file.close()

        interfaces_list = {}
        interfaces = psutil.net_if_addrs()
        interfaces_stats = psutil.net_if_stats()
        for iface in interfaces:
            if iface in interfaces_stats and interfaces[iface][0].address and interfaces[iface][1].address and \
                    interfaces[iface][1].netmask:
                iface_vendor = None
                mac_prefix = interfaces[iface][0].address.replace('-', ':')[:8]
                for vendor in self.mac_vendors:
                    if vendor['macPrefix'] == mac_prefix:
                        iface_vendor = vendor['vendorName']
                interfaces_list[iface] = {'name': iface, 'isup': interfaces_stats[iface].isup,
                                          'mac': interfaces[iface][0].address.replace('-', ':'),
                                          'ip': interfaces[iface][1].address, 'netmask': interfaces[iface][1].netmask,
                                          'vendorName': iface_vendor}

        self.interfaces = interfaces_list
