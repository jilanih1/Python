#!/usr/bin/env python
#Linux Troubleshooting script - run basic Linux commands via python script

# Modules
from __future__ import print_function
import argparse, paramiko, sys, getpass, subprocess

### for testing ###
hostname = '192.168.1.43'
username = 'root'
password = getpass.getpass('Please enter password: ')
command = 'uptime'
###################

# Global variables.
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class colors():
	red = '\033[91m'
	blu = '\033[94m'
	grn = '\033[92m'
	rst = '\033[0m'

class commands():
	uptm = 'uptime'
	free = 'free'
#	proc = 'ps -ef | grep -i ' + variable + ' | grep -v grep'
#	varm = 'grep -i ' + variable2 + ' /var/log/messages'

# Define a function for commands menu:
options = ['Check system uptime.', 'Check free memory.', 'Check if a process is running.',
	 'Check for a string in /var/log/messages.', 'EXIT']
def menu():
	print('_' * 42)
	print('Select from the following options [1-5]: ')
	for number,option in enumerate(options, 1):
		print(number, option)
	print('_' * 42)

# Define ssh & exec functions.
def connect():
	ssh.connect(hostname, port=22, username=username, password=password)

def execute():
	stdin,stdout,stderr = ssh.exec_command(command)
	type(stdin)
	print(stdout.read())

# Add options for hostname and username.
# raw_inputs for if no option is selected.

# if/else statement to ping the host
pinghost = subprocess.Popen(['ping', '-c', '1', hostname],stdout=subprocess.PIPE)
stdout, stderr = pinghost.communicate()
if pinghost.returncode == 0:
	print('' + hostname + ' is pingable, continuing...')
	try:
		connect()
		while True:
			menu()
			try:
				choice = int(input('Please select an option [1-5]: '))
				if choice == 1:
					command = commands.uptm
					print(command)
					execute()
				elif choice >1 and choice<5:
					print('Option not yet coded.')
				elif choice == 5:
					print('Exiting...')
					sys.exit(0)
				else:
					print('Invalid option selcted.')
			except (NameError, SyntaxError):
				print('Invalid option selected.')
			except (TypeError):
				print('Please enter option "5" to exit.')

	except paramiko.AuthenticationException:
		print('Authentication Failed: Please check username and password.')
	except paramiko.ssh_exception.NoValidConnectionsError:
		print('Connection Refused: Unable to connect to port 22 on ' + hostname)
else:
	print('' + hostname + ' is not pingable, please check network connectivity.')
