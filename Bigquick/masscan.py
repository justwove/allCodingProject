import argparse
import subprocess 
import os
import pickle

import json
import logging

from config import tool_path, masscan_config, top_tcp_ports, top_udp_ports
from collections import defaultdict

class Masscan():

    target_file = os.getcwd() + "/"
    rate = masscan_config.get('rate')
    interface = masscan_config.get('iface')
    

    def masscan(self, ports, projet):
        # Do something
        print("Launching masscan")
        path = self.target_file 
        file = path + f"masscan.{projet}.json"
        ips = path + f"{projet}.ips"
        command = [
            'sudo',
            tool_path.get("masscan"),
            "-v",
            "--open",
            "--banners",
            "--rate",
            self.rate,
            "-e",
            self.interface,
            "-oJ",
            file,
            "--ports",
            ports,
            "-iL",
            ips,
        ]
        print(command) 
        run = subprocess.run(command)
        if run.stderr:
            print("An error occurred:", run.stderr)
            exit()

        print("...End")
        return file

    def launching(self, jsonfile, projet):
        """ Reads masscan JSON results and creates a pickled dictionary of pertinent information for processing. """
        print("Starting to process masscan output")
        ip_dict = defaultdict(lambda: defaultdict(set))  # nested defaultdict
        masscan_json = open(jsonfile)
        path = self.target_file
        output = path + f"masscan.{projet}.parsed.pickle"
        

        try:
            entries = json.load(masscan_json)  # load masscan results from Masscan Task
        except json.decoder.JSONDecodeError as e:
            # return on exception; no output file created; pipeline should start again from
            # this task if restarted because we never hit pickle.dump
            return print(e)

        """
        build out ip_dictionary from the loaded JSON

        masscan JSON structure over which we're looping
        [
        {   "ip": "10.10.10.146",   "timestamp": "1567856130", "ports": [ {"port": 22, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 63} ] }
        ,
        {   "ip": "10.10.10.146",   "timestamp": "1567856130", "ports": [ {"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 63} ] }
        ]

        ip_dictionary structure that is built out from each JSON entry
        {
            "IP_ADDRESS":
                {'udp': {"161", "5000", ... },
                ...
                i.e. {protocol: set(ports) }
        }
        """
        for entry in entries:
            single_target_ip = entry.get("ip")
            for port_entry in entry.get("ports"):
                protocol = port_entry.get("proto")
                ip_dict[single_target_ip][protocol].add(str(port_entry.get("port")))

        with open(output, "wb") as f:
            pickle.dump(dict(ip_dict), f)
        print("...End")



if __name__ == '__main__':
    #grab the arguments when the script is ran
    parser = argparse.ArgumentParser(description='How to ?')
    parser.add_argument('--projet', required=True)
    parser.add_argument('-p', '--ports')
    parser.add_argument('--top-ports')
    args = parser.parse_args()

    if args.ports and args.top_ports:
    # can't have both
        logging.error("Only --ports or --top-ports is permitted, not both.")
        exit(1)

    if not args.ports and not args.top_ports:
        # need at least one
        logging.error("Must specify either --top-ports or --ports.")
        exit(2)

    if int(args.top_ports) < 0:
        # sanity check
        logging.error("--top-ports must be greater than 0")
        exit(3)

    if args.top_ports:
        # if --top-ports used, format the top_*_ports lists as strings and then into a proper masscan --ports option
        top_tcp_ports_str = ",".join(str(x) for x in top_tcp_ports[: int(args.top_ports)])
        top_udp_ports_str = ",".join(str(x) for x in top_udp_ports[: int(args.top_ports)])

        ports = f"{top_tcp_ports_str},U:{top_udp_ports_str}"

        masscan = Masscan()
        masscan_scan = masscan.masscan(ports, args.projet)
        masscan.launching(masscan_scan, args.projet)
        exit(1)

    masscan = Masscan()
    masscan_scan = masscan.masscan(args.ports, args.projet)
    masscan.launching(masscan_scan, args.projet)