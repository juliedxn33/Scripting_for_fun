#!/usr/bin/env python3
#scanning automation
import subprocess
import os
import sys
from pathlib import Path
import xmltodict

def Hosts_Up_Check():
	check_hosts_input_file = sys.argv[1]
	check_hosts_file = open(check_hosts_input_file, 'r')
	while True: 
		check_hosts_ip = check_hosts_file.readline()
		if not check_hosts_ip:
			break
		check_hosts_ip = check_hosts_ip.strip()
		process = subprocess.Popen(['nmap', '-sP', check_hosts_ip], stdout = subprocess.PIPE, 	universal_newlines=True)
		hosts = []
		while True:
			with open('hosts_up.txt', 'a') as f: 	 
				output = process.stdout.readline()
				hosts.append(output)
				if 'Host is up' in output:
					ip = (hosts[-2])
					ip = ip[ip.find('(')+1:ip.find(')')]
					ip = ip + "\n"
					f.write(ip)
					break
	f.close()	
	return f	
	

	
def Nmap_Scan():
	
	process = subprocess.run(['nmap', '-A', '-sV', '-p-', '-iL', 'hosts_up.txt', '-oX', 'nmap_xml_output.xml'], universal_newlines=True)
	xml_output = 'nmap_xml_output.xml'
	return xml_output

def Nmap_Clean_Up(f_name):
	with open('nmap_xml_output.xml', 'r') as xml_obj:
		nmap_dict = xmltodict.parse(xml_obj.read())
		xml_obj.close()	
		
	print(f"host info address: {nmap_dict['nmaprun']['host']['address']['@addr']}")
	print(f"host info address type: {nmap_dict['nmaprun']['host']['address']['@addrtype']}")


def main():
	hosts_up = Path('hosts_up.txt')
	nmap_scan = Path('nmap_scan.txt')
	if hosts_up.is_file():
		os.remove(hosts_up)
	if nmap_scan.is_file():
		os.remove(nmap_scan)
	Hosts_Up_Check()
	Nmap_Scan()
	Nmap_Clean_Up(Nmap_Scan())


if __name__== '__main__':
	main()		
