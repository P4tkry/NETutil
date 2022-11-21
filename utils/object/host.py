from ipaddress import IPv4Address


class Host:
    def __init__(self, mac: str = None, ip: IPv4Address = None):
        self.mac: str | None = mac
        self.netbios_name: str | None = None
        self.ip: IPv4Address | None = ip
        self.ttl: int | None = None
