import threading
import subprocess 
import os
import queue
import time
import csv

from tldextract import extract as ex

from config import tools_path as tp, top_tcp_ports as ttp, masscan_config as mg, massdns_config as mdg, api_tokens as at


# p = pathlib.Path("temp/").mkdir(parents=True, exist_ok=True)

class Scan():     

    top_ports = ttp[:100]
    
    def thread(self, command):
        try:
            thread = threading.Thread(target=subprocess.run, args=[command])
            thread.start()
            thread.join()
        except Exception as e:
            print(e)  
        
    class threadii():
        def __init__(self, command):
            self.q = queue.Queue()
            self.command = command
            self.queing()

        def worker(self):
            while True:
                item = self.q.get()
                print(f'Working on {item}')
                subprocess.run(item)
                print(f'Finished {item}')
                self.q.task_done()

        def queing(self):
            # turn-on the worker thread
            threading.Thread(target=self.worker, daemon=True).start()
            # send requests to the worker
            for item in self.command:
                self.q.put(item)
            print('All task requests sent\n', end='')
            # block until all tasks are done
            self.q.join()
            print('All work completed')

    def readfile(file, type=None):
        if type is not None:
            exit()
        with open(file, 'r') as f:
            file = f.readlines()
            return [line.strip() for line in file]

    def clean_burp_domain(self):
        with open('clean_burp_domains.txt', 'w') as f, open('burp_domains.txt') as d:
            domains = [i for i in d.readlines()]
            clean_domain = [i.replace('\n', '') for i in domains]
            root_domain = [ex(i) for i in clean_domain]
            root_domain = [f"{res[1]}.{res[2]}" if res[0] == '' else f"{res[0]}.{res[1]}.{res[2]}" for res in root_domain]
            root_domain = list(dict.fromkeys(root_domain))
            write = [f.write(i + '\n') for i in root_domain]
                
    def rename(self, from_file, to_file):
        os.rename(from_file, to_file)

    def clean_file(self, listOfFile):
        tmp = set()
        try:
            for file in listOfFile:
                with open(f'tmp_{file}', 'w') as tmp_file, open(file, 'r') as old_file:
                    for line in old_file:
                        if line not in tmp:
                            tmp_file.write(line)
                            tmp.add(line)
                os.remove(file)
            for file in listOfFile:
                self.rename(f'tmp_{file}', file)
                time.sleep(10)
        except Exception as e:
            print(e)    
    

    def setuper(self):
        print('--------------------------------')
        print('Setuping wordlist with Amass, Sublist3r & Massdns outuput')
        with open('amass.subdomains', 'r') as amass_subd, open('allsub.txt', 'a') as all:#open('sublist3r.txt', 'r') as sublist, open('massdns_domains.txt', 'r') as massdns_domains, open('allsub.txt', 'a') as all:
            amass_subd = amass_subd.readlines()
            #sublist = sublist.readlines()
            amass = [all.write(line) for line in amass_subd]
            #subl = [all.write(line) for line in sublist]
            #massdns = [all.write(line) for line in massdns_domains]
        self.clean_file(['allsub.txt'])

    def web_setuper(self):
        print('--------------------------------')
        print('Setuping WebWordlist')
        with open('allsub.txt') as all, open('web.txt', 'a') as web, open('web.csv', 'a', encoding='utf-8') as webcsv:
            run = subprocess.run([tp.get('httprobe')], stdin=all, capture_output=True, text=True)
            [web.write(line) for line in run.stdout]
            targets = list(run.stdout)
            headers = ['targets', 'Description']

        

if __name__ == '__main__':
    scan = Scan()

    wordlist = 'wordlist'
    # scan.Amass(wordlist)
    # scan.Massdns(wordlist)
    # scan.Masscan()
    # scan.sublister()
    # scan.setuper()
    # scan.web_setuper
    # scan.scanningModules()
    # scan.in_scope_targets()