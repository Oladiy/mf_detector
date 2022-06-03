from html.parser import HTMLParser


class PersonalAccountHTMLParser(HTMLParser):
    router_name: str
    devices: list

    device_number: int
    host_name: str
    mac: str
    ip: str
    interface: str

    is_device_number_parsed: bool
    is_host_name_parsed: bool
    is_mac_parsed: bool
    is_ip_parsed: bool
    is_interface_parsed: bool

    def set_parser(self, router_name: str):
        self.router_name = router_name
        self.devices = []

        self.device_number = -1
        self.host_name = ''
        self.mac = ''
        self.ip = ''
        self.interface = ''

        self.is_device_number_parsed = False
        self.is_host_name_parsed = False
        self.is_mac_parsed = False
        self.is_ip_parsed = False
        self.is_interface_parsed = False

    def retrieve_devices(self):
        devices = self.devices.copy()
        self.devices = []

        return devices

    def handle_data(self, data: str):
        if not data.strip():
            return

        if self.router_name == 'zyxel':
            self.parse_zyxel_pa_html(data)

    def parse_zyxel_pa_html(self, data: str):
        if not self.is_device_number_parsed:
            try:
                self.device_number = int(data)
                self.is_device_number_parsed = True
            except ValueError:
                ...
        elif not self.is_host_name_parsed:
            self.host_name = data
            self.is_host_name_parsed = True
        elif not self.is_ip_parsed:
            self.ip = data
            self.is_ip_parsed = True
        elif not self.is_mac_parsed:
            self.mac = data
            self.is_mac_parsed = True
        elif not self.is_interface_parsed:
            self.interface = data
            self.is_interface_parsed = True

        if self.is_interface_parsed:
            self.is_device_number_parsed = False
            self.is_host_name_parsed = False
            self.is_mac_parsed = False
            self.is_ip_parsed = False
            self.is_interface_parsed = False
            if self.interface == "lan":
                return

            self.devices.append(f"Host name: {self.host_name}\n"
                                f"Ip: {self.ip}\n"
                                f"MAC: {self.mac}\n"
                                f"Interface: {self.interface}\n"
                                "____________________________\n")
