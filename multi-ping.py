#!/usr/bin/env python3

from __future__ import print_function #Python Version Compatibility
import os, sys, subprocess #Modules

if sys.version_info[:2] <= (2, 7): #Python Version Compatibility
	input = raw_input

#Colors, Green=Pass, Red=Fail
class colors():
	Red = '\033[91m'
	Green = '\033[92m'
	Reset = '\033[0m'

#Information messages:
class info():
	nofile = 'Please select a file: '
	vafile = ' is a valid file, proceeding...'
	fafile = 'File not found. Please check filename and path, exiting...'
	pingsu = ' is pingable'
	pingfl = ' is not pingable'
	errarg = 'Too many arguments. Please select a file: '

if __name__ == '__main__':

	if len(sys.argv) == 2:
		hfile = sys.argv[1]
	elif len(sys.argv) == 1:
		hfile = input(colors.Red + info.nofile + colors.Reset)
	else:
		hfile = input(colors.Red + info.errarg + colors.Reset)

	#Checks if the argument provided is valid
	if os.path.isfile(hfile):
		print(colors.Green + hfile + info.vafile + colors.Reset)
	else:
		print(colors.Red + info.fafile + colors.Reset)
		sys.exit(1)

	#Opens the file and adds the entries to a list
	with open(hfile, 'r') as hosts:
		hostlist = [line.strip() for line in hosts]
	hosts.close()
	#for loop to ping all the entries in the list
	for ip in hostlist:
		output = subprocess.Popen(['ping', '-c', '1', ip],stdout=subprocess.PIPE)
		stdout, stderr = output.communicate()
		if output.returncode == 0:
			print(colors.Green + ip + info.pingsu + colors.Reset)
		else:
			print(colors.Red + ip + info.pingfl + colors.Reset)
sys.exit(0)

### NOTE: Hosts should be listed in the file as following (Without #) ###
#Host1
#Host2
#Host3
#Etc.
