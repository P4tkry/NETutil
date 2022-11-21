import json


def get_mac_vendor(mac: str) -> str | None:
    vendors_file = open('./data/mac-vendors.json', encoding="utf8")
    vendors = json.load(vendors_file)
    vendors_file.close()

    for vendor in vendors:
        if vendor['macPrefix'] == str(mac[:8]).upper():
            return vendor['vendorName']
    return None
