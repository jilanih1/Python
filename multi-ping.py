#!/usr/bin/env python

from __future__ import print_function #Python3 Compatibality
import os, sys, subprocess, argparse #Modules

#Colors, Green=Pass, Red=Fail
class colors():
	Red = '\033[91m'
	Green = '\033[92m'
	Reset = '\033[0m'

#Defined to make code easier to read
class info():
	nofile = 'Please select a file'
	vafile = ' is a valid file, proceeding...'
	fafile = 'File not found. Please check filename and path, exiting...'
	success = ' is pingable'
	fail = ' is not pingable'

#Allows -f + <file> while running the script to choose a file without prompt.
parser = argparse.ArgumentParser(usage='multi-ping -f <file>')
required = parser.add_argument_group('required arguments')
required.add_argument('-f', '--file', help='specify the file with full path')
args = parser.parse_args()

#Checks if an argument is provided for -f
if not args.file:
	print(colors.Red + info.nofile + colors.Reset + '\n')
	sys.exit(1)

#Checks if the argument provided is valid
if os.path.isfile(args.file):
	print(colors.Green + args.file + info.vafile + colors.Reset + '\n')
else:
	print(colors.Red + info.fafile + colors.Reset + '\n')
	sys.exit(1)

#Opens the file and adds the entries to a list
with open(args.file, 'r') as hosts:
	hostlist = [line.strip() for line in hosts]
hosts.close()

#for loop to ping all the entries in the list
for ip in hostlist:
	output = subprocess.Popen(['ping', '-c', '1', ip],stdout=subprocess.PIPE)
	stdout, stderr = output.communicate()

	if output.returncode == 0:
		print(colors.Green + ip + info.success + colors.Reset)
	else:
		print(colors.Red + ip + info.fail + colors.Reset)

print('\n')
sys.exit(0)

### NOTE: Hosts should be listed in the file as following (Without #) ###
#Host1
#Host2
#Host3
#Etc.
