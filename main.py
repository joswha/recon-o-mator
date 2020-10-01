import os
from os import path
import re
import subprocess
import argparse


def make_directory(loc):
    if not path.exists(loc):
        os.mkdir(loc)
    else:
        print("There already exists a " + loc + " directory for that target... continuing")

def check_empty_list(li, arg):
    if not li:
        print("The list for " + arg + " ports is empty... continuing")
        return True
    else:
        print("The list for " + arg + " ports is not empty... continuing")
        return False

def find_port(port_type):
    ports =  re.findall(re.compile("(\d+)\/tcp" + port_type), open("nmap/nmapAllPorts", "r").read())
    return ports

def process_finished(proc):
    if proc.poll() is not None:
        return True
    else:
        return False

def main():

    parser = argparse.ArgumentParser(description = 'Recon automation boi')

    parser.add_argument('--t', type=str, help='Target(ip address)', required=True, action="store", dest="ip")
    parser.add_argument('--n', type=str, help='Optional folder name', required=False, action="store", dest="name")
    parser.add_argument('--a', type=str, help='Full recon( nikto + enum4linux )', required=False, action="store", dest="full")

    args = parser.parse_args()

    ip = args.ip
    name = args.name
    full = args.full

    if name is not None:
        make_directory(name)
        os.chdir(name)
    else:
        make_directory(ip)
        os.chdir(ip)

    make_directory('nmap')

    first = subprocess.Popen("nmap -p- " + ip + " -oN nmap/nmapAllPorts", shell = True)

    while True:
        if first.poll() is not None:

            all_ports = ",".join(find_port('')) # ports for detailed NMAP, separated by comma
            all_ports_nojoin = find_port('')    # ports for detailed checks, NOT separated by comma

            second = subprocess.Popen("nmap -p " + all_ports + " " + ip + " -A -sV -oN nmap/nmapInDetail", shell = True)

            http_ports = find_port(".+http")    # ports for HTTP related commands, not separated by comma

            if check_empty_list(http_ports,'http') is False: # => there are http ports
                    make_directory('nikto')
                    for port in http_ports:
                        nikto = subprocess.Popen("nikto -h http://" + ip + ":" + port + " > nikto/nikto_" + port, shell = True)
                        break

            for port in all_ports_nojoin:  # check if there's any SMB related port, thus we can scan with enum4linux
                if port == '135' or port == '139' or port == '445' or port == '138':
                    make_directory('enum4linux')
                    enum4linux = subprocess.Popen("enum4linux -a " + ip + " > enum4linux/enum4linux_" + ip, shell = True)
                    break
            
            for port in all_ports_nojoin:
                if port == '22':
                    ssh_v, _ = subprocess.Popen(["nc", ip, "22"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    if float(ssh_v.split("SSH_")[1][:3]) < 7.7:
                        print("This version of ssh is vulnerable to username enumaration")
            break
        
if __name__ == "__main__":
    main()
