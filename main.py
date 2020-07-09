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
        print("There already exists a " + loc + " directory for that target... continuing")

make_directory(ip)
os.chdir(ip)

make_directory('nmap')
make_directory('nikto')
make_directory('dirsearch')

# first = subprocess.Popen("nmap " + ip + " -oN nmap/nmapAllPorts", shell = True)

def find_port(port_type):
    ports =  re.findall(re.compile("(\d+)\/tcp" + port_type), open("nmap/nmapHTTPports", "r").read())
    return ports

while True:
    if first.poll() is not None:
        all_ports = ",".join(find_port('')) # ports for detailed NMAP, separated by comma
        http_ports = find_port(".+http")    # ports for HTTP related commands, not separated by comma
    
        second = subprocess.Popen("nmap -p " + all_ports + " " + ip + " -A -sV -oN nmap/nmapInDetail", shell = True)

        for port in http_ports:
            nikto = subprocess.Popen("nikto -h http://" + ip + ":" + port + " > nikto/nikto_" + port, shell = True)
            dirsearch = subprocess.Popen("python dirsearch.py -u http://" + ip + ":" + port + " -e txt,php,js > dirsearch/dirsearch_" + port, shell = True)

        break
