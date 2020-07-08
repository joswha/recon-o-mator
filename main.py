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

if not path.exists(ip):
    os.mkdir(ip)
else:
    print("There already exists a directory for that target... continuing")

os.chdir(ip)

if not path.exists('nmap'):
    os.mkdir('nmap')
else:
    print("There already exists a nmap directory for that target... continuing")

first = subprocess.Popen("nmap -p- " + ip + " -oN nmap/nmapAllPorts", shell = True)

while True:
    if first.poll() is not None:
        ports_match = re.compile("(\d+)\/tcp")
        ports =  re.findall(ports_match, open("nmap/nmapAllPorts", "r").read())
        all_ports = ",".join(ports)

        second = subprocess.Popen("nmap -p " + all_ports + " " + ip + " -A -sV -oN nmap/nmapInDetail", shell = True)
        
        print(all_ports)
        break

# os.system("nikto -h http://" + ip + ":" + ports[0] + " > nikto")
