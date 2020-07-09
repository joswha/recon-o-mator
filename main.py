import os
from os import path
import sys
import re
import subprocess
import argparse

########################################################################################################
#                                       hey                                                            #
########################################################################################################


parser = argparse.ArgumentParser(description='Recon automation boi')

parser.add_argument('--t', type=str, help='Target(ip address)', required=True, action="store", dest="ip")

args = parser.parse_args()
ip = args.ip

def make_directory(loc):
    if not path.exists(loc):
        os.mkdir(loc)
    else:
        print("There already exists a directory for that target... continuing")

make_directory(ip)
os.chdir(ip)

make_directory('nmap')

first = subprocess.Popen("nmap " + ip + " -oN nmap/nmapAllPorts", shell = True)

def find_port(port_type):
    ports =  re.findall(re.compile("(\d+)\/tcp" + port_type), open("nmap/nmapAllPorts", "r").read())
    return ",".join(ports)

while True:
    if first.poll() is not None:
        all_ports = find_port('')
        http_ports = find_port(".+http")
        domain_ports = find_port(".+domain")
        
        # second = subprocess.Popen("nmap -p " + all_ports + " " + ip + " -A -sV -oN nmap/nmapInDetail", shell = True)
        
        print(all_ports)
        print(http_ports)
        print(domain_ports)
        break

# os.system("nikto -h http://" + ip + ":" + ports[0] + " > nikto")
