import os
import sys

ip = sys.argv[1]
optional_name = sys.argv[2]

if len(optional_name) > 0:
    os.system("mkdir " + optional_name + " & cd " + optional_name )
else: 
    os.system("mkdir " + ip + " & cd " + ip )

os.system("mkdir nmap & nmap -p- " + ip + " -oN nmap/nmapAllPorts")
os.system("nmap -A -sV " + ip + " -oN nmap/nmapInDetail")

os.system("cd ../ & nikto -h http://" + ip + ":" + port + " > nikto")

