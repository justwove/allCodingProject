import json

from scan import Scan
from config import tools_path as tp, masscan_config as mg

class Masscan():
    def __init__(self):
        self.scan = Scan()
        print('Starting masscan')
        self.masscan()
        self.masscan_parse()
        self.scan.clean_file(self.outputfile)
        print('Masscan finished.... \n\n\n\n')

    def masscan(self):
        top_ports = ",".join(repr(e) for e in self.scan.top_ports)
        command = [f'{tp.get("masscan")}','-v','--open','--banners','--rate',f'{mg.get("rate")}','-e',f'{mg.get("iface")}','-oJ','masscan.json','--ports',f'{top_ports}','-iL','amass.ips']
        self.scan.thread(command) 

    def masscan_parse(self):
        with open('masscan.json', 'r') as masscanjson:
            self.outputfile = []
            for line in masscanjson:
                if "{" in line:
                    try:
                        jsonline = json.loads(line)
                        tmp_file = open(f"{jsonline['ip']}.masscan.inital", 'a')
                        self.outputfile.append(f"{jsonline['ip']}.masscan.inital")
                        for port in jsonline['ports']:
                            for type in port:
                                if type == "service":
                                    for i, value in enumerate(port[type]):
                                        if i == 0:
                                            tmp_file.write(f"\n{type}:\n{port[type][value]}\n")
                                        else:
                                            tmp_file.write(f"{port[type][value]}\n\n")
                                else:
                                    tmp_file.write(f"{type}: {port[type]}\n")
                    except Exception as e:
                        print(e)