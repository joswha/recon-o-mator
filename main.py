import os
import sys

#directory = input("Enter your directory : ") 
#
ip = sys.argv[1]
#os = sys.argv[2]

os.system("mkdir " + ip + " & cd " + ip )
os.system("mkdir nmap & cd nmap & nmap -p- " + ip + " > nmapAllPorts")
