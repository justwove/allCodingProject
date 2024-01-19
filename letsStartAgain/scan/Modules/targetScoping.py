import subprocess
import re

from scan import Scan
from config import tools_path as tp, api_tokens as at

class targetScoping():

    def __init__(self):
        self.scan = Scan()

    def in_scope_targets(self):
        hackerone = subprocess.run([tp.get('bbscope'),'h1', '-t', at.get('hackerone'), '-u', 'wove', '-b', '-o', 't', 'd', ', ' ], capture_output=True, text=True)
        bugcrowd = subprocess.run([tp.get('bbscope'),'bc', '-t', at.get('bugcrowd'), '-b', '-o', 't', 'd', ', ' ], capture_output=True, text=True)

        h1file = open('scope.txt', 'w')
        h1file.write(hackerone.stdout)
        bcfile = open('scope.txt', 'a')
        bcfile.write(bugcrowd.stdout)
        self.scan.clean_file('scope.txt')
        self.clean_scope('scope.txt')


    def clean_scope(self, scope_file):
        try:
            file = open(scope_file, 'r')
            wordlist = open('wordlist', 'a')
            web = open('web.txt', 'a')
            allsub = open('allsub.txt', 'a')
            amassip = open('amass.ips', 'a')
            for line in file:
                if re.search('\(|github|your|NO_IN_SCOPE_TABLE|gitlab|.js| |wiki', line):
                    continue
                if re.search('^[*]|[*]$' ,line):
                    print(f'should be domains to add to wordlist: {line}')
                    wordlist.write(line)

                if re.search('^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})', line):
                    if line[-4] == '/':
                        print(f'ip with CIDR : {line}')
                        allsub.write(line)
                    else:
                        print(f'ip : {line}')
                        amassip.write(line)
                if re.search('http|https', line):
                    print(f'site to scan {line}')
                    web.write(line)
                if re.search('^[0-9]', line):
                    continue
                else:
                    print(f'domain not to scan: {line}')
        except Exception as e:
            print(e)
