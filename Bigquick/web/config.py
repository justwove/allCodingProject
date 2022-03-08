tool_path =  {
    'amass': '/snap/bin/amass',
    'masscan': '/usr/bin/masscan',
    'nmap': '/usr/bin/nmap',
    'aquatone': '/usr/local/sbin/aquatone',
    'tko-subs': '/home/seb/go/bin/tko-subs',
    'tko-subs-dir': '/home/seb/go/src/github.com/anshumanbh/tko-subs',
    'subjack': '/home/seb/go/bin/subjack',
    'subjack-fingerprints': '/home/seb/go/src/github.com/haccer/subjack/fingerprints.json',
    'gobuster': '/usr/bin/gobuster',
    'feroxbuster': '/snap/bin/feroxbuster',
    'CORScanner': '/home/seb/Tools/CORScanner/cors_scan.py',
}

masscan_config = {
    'iface': 'eth0',
    'rate': '1000',
}

web_ports = {'80', '443', '8080', '8000' '8443'}

defaults = {
    'threads': '10',
    'aquatone-scan-timeout': '900',
    'gobuster-wordlist': '/usr/share/wordlist/dirbuster/directory-list-2.3-small.txt',
}