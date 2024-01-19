import json

from config import tools_path as tp, massdns_config as mdg
from scan import Scan

class Massdns():
    def __init__(self, wordlist=None):
        if wordlist is None:
            print('Please specify a wordlist to run massdns')
        self.wordlist = wordlist
        self.scan = Scan()
        self.massdns_mutiple_run(3)
        self.scan.clean_file(self.outputfile)
        
    def massdns_mutiple_run(self, number):
        for _ in range(number):
            print('Starting massdns scan...')
            self.massdns(self.wordlist)
            self.massdns_parse()
            print('Scan completed... \n\n\n\n')

    def massdns(self, wordlist):
        commands = [tp.get("massdns"),'-o','J','-w','massdns.json','-r',mdg.get('resolver'), wordlist]
        self.scan.thread(commands)
        self.outputfile = ['massdns.ips', 'massdns.ip6s', 'massdns.nameservers', 'massdns.domains']

    def massdns_parse(self):
        with open('massdns.json', 'r') as massdnsjson, open('massdns_domains.txt', 'a') as domain_file, open('massdns_ipv4.txt', 'a') as ipv4_file, open('massdns_ipv6.txt', 'a') as ipv6_file, open('massdns_resolver.txt', 'a') as resolver_file:
            for line in massdnsjson:
                jsonline = json.loads(line)
                data = jsonline['data']
                for datas in data:
                    for info in data[datas]:
                        for test in info:
                            if test == "name":
                                domain_file.write(info[test][:-1] + "\n")
                            if test == "data":
                                if info['type'] == "A":
                                    ipv4_file.write(info[test] + "\n")
                                    continue
                                if ":" in info[test]:
                                    ipv6_file.write(info[test] + "\n")
                                    continue
                                domain_file.write(info[test][:-1] + "\n")
                resolver_file.write(jsonline['resolver'] + "\n")    
        self.outputfile = ['massdns_domains.txt', 'massdns_ipv4.txt', 'massdns_ipv6.txt', 'massdns_resolver.txt']
        self.scan.clean_file(self.outputfile)