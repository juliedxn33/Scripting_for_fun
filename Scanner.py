#!/usr/bin/env python3
#scanning automation
import subprocess
import os
import sys
from pathlib import Path
import xmltodict
import pandas as pd

#uses nmap -sP to check if hosts are live and saves corresponding hosts to hosts_up.txt
def Hosts_Up_Check(hosts_input_file):
	check_hosts_input_file = hosts_input_file
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
	

#launches a verbose nmap scan on the hosts in the "hosts_up.txt", scans all ports (tcp only) and outputs results into an xml file
def Nmap_Scan():
	process = subprocess.run(['nmap', '-A', '-sV', '-v', '-p-', '-iL', 'hosts_up.txt', '-oX', 'nmap_xml_output.xml'], universal_newlines=True)
	xml_output = 'nmap_xml_output.xml'
	return xml_output

#cleans up "nmap_xml_output.xml" by using xmltodict library to parse data into a dict. 
#The dict results are stored in a readable csv file. Full functionality is still being worked on.
def Nmap_Clean_Up():
	with open('nmap_xml_output.xml', 'r') as xml_obj:
		nmap_dict = xmltodict.parse(xml_obj.read())
		xml_obj.close()	
		
	with open('xmltocsv_tool_output', 'w') as xml_debug:
		xml_debug.write(str(nmap_dict))	
	
	#TODO development has been done nmapping only localhost due to lack of lab environment, how to accommodate multiple hosts?
			
	rows = []
	cols = ["Host Address", "Address Type", "Hostname", "Port", "Protocol", "State"]
	
	#troubleshooting print statements	
	#print(f"host info address: {nmap_dict['nmaprun']['host']['address']['@addr']}")
	#print(f"host info address type: {nmap_dict['nmaprun']['host']['address']['@addrtype']}")
	#print(f"host info hostname: {nmap_dict['nmaprun']['host']['hostnames']['hostname']['@name']}")
	
	addr = str({nmap_dict['nmaprun']['host']['address']['@addr']})
	addr = addr.strip("{}")
	addrtype = str({nmap_dict['nmaprun']['host']['address']['@addrtype']})
	addrtype = addrtype.strip("{}")
	name = str({nmap_dict['nmaprun']['host']['hostnames']['hostname']['@name']})
	name = name.strip("{}")
	#TODO cycle through x ports for all port info
	try:
		
		#troubleshooting print statements
		#print(f"host info port: {nmap_dict['nmaprun']['host']['ports']['port']['@portid']}")
		#print(f"host info protocol: {nmap_dict['nmaprun']['host']['ports']['port']['@protocol']}")
		#print(f"host info state: {nmap_dict['nmaprun']['host']['ports']['port']['state']['@state']}")
		
		
		portid = str({nmap_dict['nmaprun']['host']['ports']['port']['@portid']})
		portid = portid.strip("{}")
		protocol = str({nmap_dict['nmaprun']['host']['ports']['port']['@protocol']})
		protocol = protocol.strip("{}")
		state = str({nmap_dict['nmaprun']['host']['ports']['port']['state']['@state']})
		state = state.strip("{}")
		
		rows.append({"Host Address": addr, "Address Type": addrtype, "Hostname": name, "Port": portid, "Protocol": protocol, "State" : state})
              
	
	except KeyError:
		print("Sometimes xml does weird dict stuff this might be one of those times")


	df = pd.DataFrame(rows, columns=cols)
	# Writing dataframe to csv
	df.to_csv('xml_to_csv_output.csv')



def main():
	hosts_up = Path('hosts_up.txt')
	nmap_scan = Path('nmap_scan.txt')
	if hosts_up.is_file():
		os.remove(hosts_up)
	if nmap_scan.is_file():
		os.remove(nmap_scan)
	#fully automated option where input is just a text file with ipv4 hosts
	full_auto = "-a"	
	if sys.argv[1] == full_auto:
		try:
			check_hosts_input_file = sys.argv[2]	
			Hosts_Up_Check(check_hosts_input_file)
			Nmap_Scan()
			Nmap_Clean_Up()
		except IndexError:
			print("Text file with hosts missing")
			exit()
			

if __name__== '__main__':
	main()		
