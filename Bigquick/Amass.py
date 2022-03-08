import argparse
import subprocess 
import os

import json
import ipaddress

from config import tool_path

class Amass():

    target_file = os.getcwd() + "/"

    def amass_scan(self, wordlist, projet):
        # Do something
        print("Launching the Amass Scan")
        path = self.target_file 
        file = path + f"amass.{projet}.json"
        command = [
            tool_path.get("amass"),
            "enum",
            "-active",
            "-ip",
            "-brute",
            "-min-for-recursive",
            "3",
            "-df",
            wordlist,
            "-json",
            file,
        ]
        run = subprocess.run(command, capture_output=True, text=True)
        if run.stderr:
            print("An error occurred:", run.stderr)

        print(file)
        print("...Done")
        return file

    def output(self, projet):
        """ Returns the target output files for this task.

        Naming conventions for the output files are:
            TARGET_FILE.ips
            TARGET_FILE.ip6s
            TARGET_FILE.subdomains

        Returns:
            dict(str: luigi.local_target.LocalTarget)
        """
        return [
            f"{self.target_file}{projet}.ips",
            f"{self.target_file}{projet}.ip6s",
            f"{self.target_file}{projet}.subdomains",
            f"{self.target_file}{projet}.asns", 
        ]

    def test_ip(self, unique_ips, unique_ip6s, unique_asns, entry):
        for address in entry.get("addresses"):
            ipaddr = address.get("ip")
            if isinstance(ipaddress.ip_address(ipaddr), ipaddress.IPv4Address):
                unique_ips.add(ipaddr)
            elif isinstance(ipaddress.ip_address(ipaddr), ipaddress.IPv6Address):
                unique_ip6s.add(ipaddr)
            asn = address.get("asn")
            unique_asns.add(asn)

    def launching(self, jsonfile, projet):
        """ Parse the json file produced by AmassScan and categorize the results into ip|subdomain files.

        An example (prettified) entry from the json file is shown below
            {
                "Timestamp": "2019-09-22T19:20:13-05:00",
                "name": "beta-partners.tesla.com",
                "domain": "tesla.com",
                "addresses": [
                {
                    "ip": "209.133.79.58",
                    "cidr": "209.133.79.0/24",
                    "asn": 394161,
                    "desc": "TESLA - Tesla"
                }
                ],
                "tag": "ext",
                "source": "Previous Enum"
            }
        """
        print("Starting to process the amass output")
        unique_ips, unique_ip6s, unique_subs, unique_asns = set()
        ip_file, ip6_file, subdomain_file, asn_file = self.output(projet)

        with open(jsonfile, 'r') as f, open(ip_file, 'w') as i, open(ip6_file, 'w') as i6, open(subdomain_file, 'w') as s, open(asn_file, 'w') as a:
            amass_json = f.readlines()
            print("First Stage")
            for line in amass_json:                
                if "{" in line:
                    entry = json.loads(line)
                    unique_subs.add(entry.get("name"))

                    self.test_ip(unique_ips, unique_ip6s, unique_asns, entry)

                    # send gathered results to their appropriate destination

                    for ip in unique_ips:
                        print(ip, file=i)

                    for sub in unique_subs:
                        print(sub, file=s)

                    for ip6 in unique_ip6s:
                        print(ip6, file=i6)

                    for asns in unique_asns:
                        print(asns, file=a)
            print("...Done")
            print("""Please check the asn scan output manually, we don't want to hack Google or amazon
            will add an filter with them to automate later""")
            return True

if __name__ == '__main__':
    #grab the arguments when the script is ran
    parser = argparse.ArgumentParser(description='How to ?')
    parser.add_argument('-w', '--wordlist', required=True)
    parser.add_argument('-p', '--projet', required=True)
    args = parser.parse_args()
    amass = Amass()
    try:
        amass_scan = amass.amass_scan(wordlist=args.wordlist, projet=args.projet)
        amass.launching(amass_scan, args.projet)
    except Exception as e:
        print(e)