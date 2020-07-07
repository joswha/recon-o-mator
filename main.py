import os
import sys
import re

ip = sys.argv[1]

#optional_name = sys.argv[2]

#if len(optional_name) > 0:
#   os.system("mkdir " + optional_name + " & cd " + optional_name )
#else:
os.system("mkdir " + ip + " ; cd " + ip )

os.system("mkdir nmap ; nmap -p- " + ip + " -oN nmap/nmapAllPorts")
os.system("nmap -A -sV " + ip + " -oN nmap/nmapInDetail")

ports_match = re.compile("(\d+)\/tcp")
ports =  re.findall(ports_match, open("nmap/nmapAllPorts", b"r").read())
print(ports)
os.system("nikto -h http://" + ip + ":" + ports[0] + " > nikto")

