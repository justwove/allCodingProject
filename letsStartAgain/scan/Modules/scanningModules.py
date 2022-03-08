import subprocess
import os
from sys import setrecursionlimit

from scan import Scan
from config import tools_path as tp

class scanningModules():

    setrecursionlimit(10000)

    def __init__(self):
        self.scan = Scan()
        self.outputfile = []
        self.torun = []
        allsub = open('allsub.txt', 'r')
        targets = [line.strip() for line in allsub.readlines()]
        print(targets)
        print('--------------------------------')
        print('Launching waybackurls')
        self.waybackurls()
        print('...Done')
        print('--------------------------------')
        print('Launching rustScan')
        self.rustScan(targets)
        print('...Done')
        print('--------------------------------')
        print('Launching searchploit with rustScan results')
        [self.searchsploit(target) for target in targets]
        print('...Done')
        # self.wafwoof(targets)
        # self.googler()
        print('--------------------------------')
        print('Launching subjack')
        self.subjack()
        print('...Done')
        print('--------------------------------')
        print('Laucnhing gau')
        self.gau()
        print('...Done')
        self.scan.clean_file(self.outputfile)


    def waybackurls(self):
        command = subprocess.run([tp.get("waybackurls")], stdin=open('allsub.txt'), capture_output=True, text=True)
        if command.stderr:
            exit()
        with open('waybackurls.txt', 'a') as f:
            write = f.write(command.stdout) 
        self.outputfile.append('waybackurls.txt')

    def rustScan(self, targets):
        top_ports = ",".join(repr(e) for e in self.scan.top_ports)
        commands = [[tp.get('rustScan'),'-a',target,'-p',top_ports,'--ulimit','5000','--','-sV','-sC','-oX',f'{target}.initial.xml'] for target in targets]
        [self.scan.thread(command) for command in commands]
        [self.outputfile.append(f'{target}.initial') for target in targets]


    def googler(self):
        commands = [[tp.get('googler'),'-n','15','-t','m14','-w','imdb.com','jungle','book'], [tp.get('googler'), '"Awoui', 'Tous', 'droits', 'réservés"', 'in', 'spring', '-t', 'm14'], [tp.get('googler'), '"Awoui', 'Copyright"', 'in', 'spring', '-t', 'm14'], [tp.get('googler'), '"Awoui', '©"', 'in', 'spring', '-t', 'm14']]    

    def subjack(self):
        commands = [tp.get('subjack'), '-w', 'allsub.txt', '-t', '100', '-timeout', '30', '-o', 'subjack.txt', '-ssl', '-c', '/home/seb/go/src/github.com/haccer/subjack/fingerprints.json']
        [self.scan.thread(command) for command in commands]
        self.outputfile.append('subjack.txt')
    
    class gau():

        def __init__(self):
            self.scan = Scan()
            self.allsub = open('allsub.txt', 'r')
            targets = [line.strip() for line in self.allsub.readlines()]
            self.gau(targets)
            self.scan.clean_file('gau.txt')

        def gau(self, all_targets):
            commands = [[tp.get('gau'),'--json','--fc','404,302',target,'--subs','--threads','5'] for target in all_targets]
            self.gau_parse(commands)

        def gau_parse(self, commands):
            tmp = []
            for command in commands:
                run = subprocess.run(command, capture_output=True, text=True)
                [print(f"An error occured : {run.stderr}") if run.stderr else None]
                tmp.append(run.stdout)
                outputfile = tmp[0].split('\n')
                for line in outputfile:
                    line = line.strip('{"url": "}')
                    with open('gau.txt', 'a') as f:
                        f.write(line + "\n")
    
    def searchsploit(self, target):
        command = [tp.get('searchsploit'),'-w','-v','--nmap',f'{target}.initial.xml']
        run = subprocess.run(command, capture_output=True, text=True)
        if (
            'XPath' not in run.stderr
            and 'Could not find file' not in run.stderr
            and '-' in run.stdout
        ):
            with open(f'{target}.exploit', 'a') as f:
                write = f.write(run.stdout)

    def sublister(self):
        amassub = open('amass.subdomains', 'r')
        targets = [line.strip() for line in amassub.readlines()]
        commands = [['python3', tp.get('sublister'), '-d', target, '-v', '-t', '10', '-o', f'{target}.sublist3r.txt'] for target in targets]
        print('Starting sublist3r search')
        self.scan.threadii(commands)
        print('Ending sublist3r search... \n\n\n')
        for target in targets:
            with open(f'{target}.sublist3r.txt', 'r') as f, open('sublist3r.txt', 'a') as subl:
                targetfile = f.readlines()
                sublister = [subl.write(line) for line in targetfile]
                os.remove(f'{target}.sublist3r.txt')
