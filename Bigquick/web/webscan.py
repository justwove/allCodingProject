import subprocess
import pickle
import os 
import argparse

import logging
import ipaddress

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from config import tool_path, web_ports, defaults

class webscan():  

    output_path = os.getcwd() + "/web"
    output_file = output_path + "/web_target"

    threads = defaults.get('threads')
    scan_timeout = defaults.get("aquatone-scan-timeout")
               
    def init_web(self, projet):
        path = os.getcwd() + "/"
        target_ips = f"{path}{projet}.ips"
        target_ips6 = f"{path}{projet}.ip6s"
        target_subdomains = f"{path}{projet}.subdomains"
        amass = [target_ips, target_ips6, target_subdomains]

        """ Gather all potential web targets into a single file to pass farther down the pipeline. """

        targets = set()

        masscan = os.getcwd() + f"/masscan.{projet}.parsed.pickle"
        ip_dict = pickle.load(open(masscan, "rb"))

        """
        structure over which we're looping
        {
            "IP_ADDRESS":
                {'udp': {"161", "5000", ... },
                ...
                i.e. {protocol: set(ports) }
        }
        """

        for target, protocol_dict in ip_dict.items():
            for protocol, ports in protocol_dict.items():
                for port in ports:
                    if protocol == 'udp':
                        continue
                    if port == "80":
                        targets.add(target)
                    elif port in web_ports:
                        targets.add(f"{target}:{port}")
        i = 0
        for amass_result in amass:
            print(amass_result)
            with open(amass_result) as f:
                for target in f:
                    # we care about all results returned from amass
                    targets.add(target.strip())
                i += 1
                if i == len(amass):
                    break

        with open(self.output_file, "w") as f:
            for target in targets:
                f.write(f"{target}\n")

    def aquatone (self):
        """ Defines the options/arguments sent to aquatone after processing.
    
        cat webtargets.tesla.txt | /opt/aquatone -scan-timeout 900 -threads 20

        Returns:
            list: list of options/arguments, beginning with the name of the executable to run
        """
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        output_file = self.output_path + "/aquatone"

        command = [
            tool_path.get("aquatone"),
            "-scan-timeout",
            self.scan_timeout,
            "-threads",
            self.threads,
            "-silent",
            "-out",
            output_file,
        ]

        with open(self.output_file) as target_list:
            subprocess.run(command, stdin=target_list)

    def corscanner(self, projet):
        """ Use CORScanner to scan for potential CORS misconfigurations.

        CORScanner commands are structured like the example below.

        python cors_scan.py -i webtargets.tesla.txt -t 100

        An example of the corresponding luigi command is shown below.

        PYTHONPATH=$(pwd) luigi --local-scheduler --module recon.web.corscanner CORScannerScan --target-file tesla --top-ports 1000 --interface eth0

        Install: 
            git clone https://github.com/chenjj/CORScanner.git
            cd CORScanner
            pip install -r requirements.txt
            pip install future

        Args:
            threads: number of threads for parallel subjack command execution
            exempt_list: Path to a file providing blacklisted subdomains, one per line. *--* Optional for upstream Task
            top_ports: Scan top N most popular ports *--* Required by upstream Task
            ports: specifies the port(s) to be scanned *--* Required by upstream Task
            interface: use the named raw network interface, such as "eth0" *--* Required by upstream Task
            rate: desired rate for transmitting packets (packets per second) *--* Required by upstream Task
            target_file: specifies the file on disk containing a list of ips or domains *--* Required by upstream Task
        """
        output_file = self.output_path + f"/corscanner.{projet}.json"

        command = [
            "python3",
            tool_path.get("CORScanner"),
            "-i",
            self.output_file,
            "-t",
            self.threads,
            "-o",
            output_file,
        ]

        subprocess.run(command)


    def gobuster(self, projet,recursive):
        """ Use gobuster to perform forced browsing.

        gobuster commands are structured like the example below.

        gobuster dir -q -e -k -t 20 -u www.tesla.com -w /usr/share/seclists/Discovery/Web-Content/common.txt -p http://127.0.0.1:8080 -o gobuster.tesla.txt -x php,html

        An example of the corresponding luigi command is shown below.

        PYTHONPATH=$(pwd) luigi --local-scheduler --module recon.web.gobuster GobusterScan --target-file tesla --top-ports 1000 \
                                --interface eth0 --proxy http://127.0.0.1:8080 --extensions php,html \
                                --wordlist /usr/share/seclists/Discovery/Web-Content/common.txt --threads 20

        Install:
            go get github.com/OJ/gobuster
            git clone https://github.com/epi052/recursive-gobuster.git

        Args:
            threads: number of threads for parallel gobuster command execution
            wordlist: wordlist used for forced browsing
            extensions: additional extensions to apply to each item in the wordlist
            recursive: whether or not to recursively gobust the target (may produce a LOT of traffic... quickly)
            exempt_list: Path to a file providing blacklisted subdomains, one per line. *--* Optional for upstream Task
            top_ports: Scan top N most popular ports *--* Required by upstream Task
            ports: specifies the port(s) to be scanned *--* Required by upstream Task
            interface: use the named raw network interface, such as "eth0" *--* Required by upstream Task
            rate: desired rate for transmitting packets (packets per second) *--* Required by upstream Task
            target_file: specifies the file on disk containing a list of ips or domains *--* Required by upstream Task
        """

        commands = list()
        output_file = self.output_path + f"/gobuster-{projet}-results"

        with open(self.output_file) as file:
            for target in file:
                target = target.strip()

                try:
                    if isinstance(ipaddress.ip_address(target), ipaddress.IPv6Address):  # ipv6
                        target = f"[{target}]"
                except ValueError:
                    # domain names raise ValueErrors, just assume we have a domain and keep on keepin on
                    pass

                for url_scheme in ("https://", "http://"):
                    if recursive == 1:
                        command = [
                            tool_path.get("feroxbuster"),
                            "-u",
                            f"{url_scheme}{target}",
                            "-w",
                            defaults.get("gobuster-wordlist", ""),
                            "-x",
                            "js,html",
                            "-x",
                            "php",
                            "txt",
                            "json,docx",                            
                        ]
                    else:
                        command = [
                            tool_path.get("gobuster"),
                            "dir",
                            "-q",
                            "-e",
                            "-k",
                            "-u",
                            f"{url_scheme}{target}",
                            "-w",
                            defaults.get("gobuster-wordlist", ""),
                            "-o",
                            Path(output_file).joinpath(
                                f"gobuster.{url_scheme.replace('//', '_').replace(':', '')}{target}.txt"
                            ),
                        ]

                    #if self.extensions:
                    #    command.extend(["-x", self.extensions])
#
                    #if self.proxy:
                    #    command.extend(["-p", self.proxy])
#
                    commands.append(command)

        Path(output_file).mkdir(parents=True, exist_ok=True)

        #if self.recursive:
        #    # workaround for recursive gobuster not accepting output directory
        #    cwd = Path().cwd()
        #    os.chdir(self.output().path)
#
        with ThreadPoolExecutor(max_workers=int(self.threads)) as executor:
            executor.map(subprocess.run, commands)

        #if self.recursive:
        #    os.chdir(str(cwd))

    def tkosubs(self, projet):
        """ Defines the options/arguments sent to tko-subs after processing.

        Returns:
            list: list of options/arguments, beginning with the name of the executable to run
        """
        command = [
            tool_path.get("tko-subs"),
            f"-domains={self.output_file}",
            f"-data={tool_path.get('tko-subs-dir')}/providers-data.csv",
            f"-output={self.output_path}/tkosubs{projet}.csv",

        ]
        print(command)
        subprocess.run(command)

    def subjack(self, threads, projet):
        """ Defines the options/arguments sent to subjack after processing.

        Returns:
            list: list of options/arguments, beginning with the name of the executable to run
        """

        command = [
            tool_path.get("subjack"),
            "-w",
            self.output_file,
            "-t",
            threads,
            "-a",
            "-timeout",
            "30",
            "-o",
            f"{self.output_path}/subjack{projet}.txt",
            "-v",
            "-ssl",
            "-c",
            tool_path.get("subjack-fingerprints"),
        ]
        print(command)

        subprocess.run(command)

if __name__ == '__main__':
    #grab the arguments when the script is ran
    parser = argparse.ArgumentParser(description='How to ?')
    parser.add_argument('-p', '--projet', required=True)
    args = parser.parse_args()
    web_scan = webscan()
    # web_scan.init_web(args.projet)
    # web_scan.aquatone()
    # web_scan.corscanner(args.projet)
    # web_scan.gobuster(args.projet, 1)
    web_scan.tkosubs(args.projet)
    web_scan.subjack(10, args.projet)