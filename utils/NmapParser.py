import xml.etree.ElementTree as XMLparser
import re


class NmapParser:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.f = ''.join(f.readlines())

    def parse_xml(self) -> dict:
        # Get online hosts
        hosts = dict()

        root = XMLparser.fromstring(re.sub(r'&#([a-zA-Z0-9]+);?', r'[#\1;]', self.f))

        for host in root.iter('host'):
            if root.attrib['scanner'] == 'nmap' and host.find('status').attrib['state'] == 'down':
                continue

            ip = host.find('./address/[@addrtype="ipv4"]').attrib['addr']

            try:
                mac = host.find('./address/[@addrtype="mac"]').attrib['addr']
            except AttributeError:
                mac = ""

            try:
                hostname = host.find('./*/hostname').attrib['name']
            except AttributeError:
                hostname = ""

            try:
                os = host.find('./os/osmatch/osclass').attrib['osfamily']
            except AttributeError:
                os = "unknown"

            if not ip in hosts.keys():
                hosts[ip] = {'ip': ip, 'hostname': hostname, 'mac': mac, 'os': os, 'ports': {'tcp': {},'udp': {}}}

            # Get open ports
            for port in host.iter('port'):
                if port.find('state').attrib['state'] == 'open':
                    service = port.find('./service')
                    description = ""
                    if service is not None:
                        if 'product' in service.attrib.keys():
                            description = service.attrib['product']
                        else:
                            description = service.attrib['name']

                        if 'version' in service.attrib.keys():
                            description += f" {service.attrib['version']}"
                        if 'extrainfo' in service.attrib.keys():
                            description += f" ({service.attrib['extrainfo']})"

                    # if root.attrib['scanner'] == 'nmap':
                    hosts[ip]['ports'][port.attrib['protocol']].update({port.attrib['portid']:{'status':'open', 'description': description}})
                    # if root.attrib['scanner'] == 'masscan': # In masscan, there is one line per port
                    #     hosts[ip]['ports'][port.attrib['protocol']][port.attrib['portid']] = {'status':'open', 'description': description}

        return hosts

    def parse_nmap(self) -> dict:
        """
        From a .nmap file, search data related to target, and return as string
        @return: dict
        """

        if not self.f:
            return ""

        blacklist = ["Read data files from: ", "Please report any incorrect results at", "Nmap done at"]

        string_parsing = ""
        for line in self.f.split('\n'):
            # Remove comments
            if line.startswith('#'):
                continue
            # Remove useless elements
            if any(unwanted_element in line for unwanted_element in blacklist):
                continue
            string_parsing += line + '\n'

        scan_results = string_parsing.split('Nmap scan report for ')[1:]

        # Filtering down hosts
        alive_hosts = list(filter(lambda i: '[host down]\n' not in i, scan_results))

        hosts = dict()
        for host_scan in alive_hosts:
            ip = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', host_scan.split('\n')[0])[0]
            hosts[ip] = '\n'.join(host_scan.split('\n')[1:])

        return hosts
