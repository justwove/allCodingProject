import argparse
import subprocess 

import os
import pickle
import threading

from config import tool_path
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, wait

class Nmap():

    output_path = os.getcwd() + "/nmap/"
    
    def nmap_scan(line):
        try:
                thread = threading.Thread(target=subprocess.run, args=[line])
                print(thread)
                thread.start()
                thread.join()
                print("done")
        except Exception as e:
            print(e)

    def init_cmd(self, nmap_command, commands, target, protocol_dict):
        for protocol, ports in protocol_dict.items():
            tmp_cmd = nmap_command[:]
            tmp_cmd[2] = "-sT" if protocol == "tcp" else "-sU"

                # arg to -oA, will drop into subdir off curdir
            tmp_cmd2 = tmp_cmd[:9]
            tmp_cmd2.extend(ports)
            commands.append(tmp_cmd2)
                
            for command in commands:
                command.append(tmp_cmd[-1])
                command.append(f"{self.output_path}nmap.{target}-{protocol}")
                command.append(target)  # target as final arg to nmap

    def launching(self, threads, projet):
        print("Starting to launch nmap scans")
        input_file = os.getcwd() + f"/masscan.{projet}.parsed.pickle"
        ip_dict = pickle.load(open(input_file, "rb"))

        nmap_command = [  # placeholders will be overwritten with appropriate info in loop below
            tool_path.get("nmap"),
            "--open",
            "PLACEHOLDER-IDX-2",
            "-sC",
            "-T",
            "4",
            "-sV",
            "-Pn",
            "-p",
            "PLACEHOLDER-IDX-10",
            "-oA",
        ]

        """
        ip_dict structure
        {
            "IP_ADDRESS":
                {'udp': {"161", "5000", ... },
                ...
                i.e. {protocol: set(ports) }
        }
        """
        commands = []
        for target, protocol_dict in ip_dict.items():
            self.init_cmd(threads, nmap_command, commands, target, protocol_dict)

        # basically mkdir -p, won't error out if already there
        Path(self.output_path).mkdir(parents=True, exist_ok=True)

        try:
            executor = ProcessPoolExecutor(threads)
            future = [executor.submit(Nmap.nmap_scan, line) for line in commands]
            wait.future

        except Exception as e:
            print(e)
        print("...Done")

if __name__ == '__main__':
    #grab the arguments when the script is ran
    parser = argparse.ArgumentParser(description='How to ?')
    parser.add_argument('-p', '--projet', required=True)
    parser.add_argument('-t', '--threads', default=10)
    args = parser.parse_args()
    nmap = Nmap()
    nmap.launching(int(args.threads), args.projet)
   