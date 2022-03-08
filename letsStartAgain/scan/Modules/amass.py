import ipaddress
import json
import shlex

from scan import Scan
from config import tools_path as tp

class Amass():
    def __init__(self, wordlist=None):
        if wordlist is None:
            print('Please specify a wordlist to run Amass')
            exit(1)
        self.wordlist = wordlist
        self.scan = Scan()
        self.amass_mutiple_run(3)
        self.scan.clean_file(self.outputfile)
    
    def amass_mutiple_run(self, number):
        for _ in range(number):
            print('Starting Amass scan...')
            self.amass_run()
            self.amass_parse()
            print('Amass completed \n\n\n\n')

    def amass_run(self):
        command = shlex.split(f"{tp.get('amass')} enum -active -ip -brute -min-for-recursive 3 -df {self.wordlist} -json amass.json")
        self.scan.thread(command)
        self.outputfile = ['amass.ips', 'amass.ip6s', 'amass.subdomains', 'amass.asns']

    def test_ip(self, entry):
        for address in entry.get("addresses"):
            ipaddr = address.get("ip")
            if isinstance(ipaddress.ip_address(ipaddr), ipaddress.IPv4Address):
                self.unique_ips.add(ipaddr)
            elif isinstance(ipaddress.ip_address(ipaddr), ipaddress.IPv6Address):
                self.unique_ip6s.add(ipaddr)
            asn = address.get("asn")
            self.unique_asns.add(asn)
    
    def setup_output_file(self, i, i6, s, a, line):
        entry = json.loads(line)
        self.unique_subs.add(entry.get("name"))

        self.test_ip(entry)

        [print(ip, file=i) for ip in self.unique_ips]
        [print(ip6, file=i6) for ip6 in self.unique_ip6s]
        [print(sub, file=s) for sub in self.unique_subs]
        [print(asns, file=a) for asns in self.unique_asns]

    def amass_parse(self):
        ip4, ip6, subd, asns = self.outputfile
        self.unique_ips = set()
        self.unique_ip6s = set()
        self.unique_subs = set()
        self.unique_asns = set()
        with open('amass.json', 'r') as f, open(ip4, 'a') as i, open(ip6, 'a') as i6, open(subd, 'a') as s, open(asns, 'a') as a:
            amass_json = f.readlines()
            for line in amass_json:                
                if "{" in line:
                    self.setup_output_file(i, i6, s, a, line)