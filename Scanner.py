#scanning automation
import subprocess
import os
import sys

string_HU = 'Host is up'
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
		with open('hosts_up.txt', 'w') as file: 	 
			output = process.stdout.readline()
			hosts.append(output)
			if string_HU in output:
				ip = (hosts[-2])
				ip = ip[ip.find('(')+1:ip.find(')')]
				ip = ip + "\n"
				file.write(ip)

file.close()	

hosts_up_file = open('hosts_up.txt', 'r')

while True: 
	hosts_up_ip = hosts_up_file.readline()
	if not hosts_up_ip:
		break
	hosts_up_ip = hosts_up_ip.strip()
	with open('nmap_scan.txt', 'a') as file:
		print(f"hosts up: {hosts_up_ip}")
		file.write(hosts_up_ip)
		process = subprocess.run(['nmap', '-A', '-sV', '-p-', hosts_up_ip], capture_output=True, text=True)
		file.write(process.stdout)

		#output = process.readline()
		#if 'Port' in output:
		#	port_info = process.readline()
		#	file.write(port_info)
			
