import argparse
import logging
import threading

from Amass import Amass
from config import top_tcp_ports, top_udp_ports
from  masscan import Masscan
from nmap import Nmap

import web.config
from web.webscan import webscan

from concurrent.futures import ProcessPoolExecutor, wait


def scanning(scans):
    try:
        thread = threading.Thread(target=scans)
        print(thread)
        thread.start()
        thread.join()
        print("done")
    except Exception as e:
        print(e)



if __name__ == '__main__':

    #grab the arguments when the script is ran
    parser = argparse.ArgumentParser(description='How to ?')
    parser.add_argument('--projet', required=True)
    parser.add_argument('-p', '--ports')
    parser.add_argument('--top-ports')
    parser.add_argument('-aw', help="Amass Wordlist", required=True)
    parser.add_argument("--threads", required=True)

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


    amass = Amass()
    amass = amass.amass_scan(args.aw, args.projet)
    parse_amass = amass.launching(amass, args.projet)
    masscan = Masscan()
    masscan = masscan.masscan(args.ports, args.projet)
    parse_masscan = masscan.launching(masscan, args.projet)
    nmap = Nmap()
    nmap = nmap.launching(args.threads, args.projet)
    webscans = webscan()
    init_web = webscans.init_web(args.projet)
    aquatone = webscans.aquatone()
    corscanner = webscans.corscanner(args.projet)
    gobuster = webscans.gobuster(args.projet, recursive=1)
    tkosubs = webscans.tkosubs(args.projet)
    subjack = webscans.subjack(10, args.projet)

     
    
    
    if parse_amass is True:
        if parse_masscan is True:
            try:
                scan = [nmap, init_web]
                executor = ProcessPoolExecutor(args.threads)
                future = [executor.submit(scanning, scans) for scans in scan]
                wait.futture

            except Exception as e:
                print(e)
                exit(1)

            try:
                scan = [aquatone, corscanner, gobuster, tkosubs, subjack]
                executor = ProcessPoolExecutor(args.threads)
                future = [executor.submit(scanning, scans) for scans in scan]
                wait.futture

            except Exception as e:
                print(e)
                exit(1)


            
