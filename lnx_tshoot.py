#!/usr/bin/env python
#Linux Troubleshooting script - run basic Linux commands via python script

# Modules
from __future__ import print_function
import argparse, paramiko, sys, getpass, subprocess

### for testing: ###
hostname = '192.168.1.48'
username = 'root'
password = getpass.getpass('Please enter password: ')

### To do: ###
# Add options for hostname and username.
# raw_inputs for if no option is selected.
# Add colors

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
	proc = 'ps -ef | grep -v grep | grep -i '
	varm = 'cat /var/log/messages | grep -i '

# Defines a function for commands menu:
options = ['Check system uptime.', 'Check free memory.', 'Check if a process is running.',
	 'Check for a string in /var/log/messages.']
def menu():
	print('-' * 50)
	for number,option in enumerate(options, 1):
		print(number, option)
	print('-' * 50)

# Defines exec function.
def execute():
	print(command)
	stdin,stdout,stderr = ssh.exec_command(command)
	type(stdin)
	print(stdout.read())


# if/else statement to ping the host
pinghost = subprocess.Popen(['ping', '-c', '1', hostname],stdout=subprocess.PIPE)
stdout, stderr = pinghost.communicate()
if pinghost.returncode == 0:
	print('' + hostname + ' is pingable, continuing...')
	try:
		ssh.connect(hostname, port=22, username=username, password=password)
		while True:
			menu()
			try:
				choice = int(input('Select an options [1-4] or type "exit": '))
				if choice == 1:
					command = commands.uptm
				elif choice == 2:
					command = commands.free
				elif choice == 3:
					var = raw_input('Please enter process: ')
					command = commands.proc + var
				elif choice == 4:
					var = raw_input('Please enter string: ')
					command = commands.varm + var
				else:
					command = null
					print('Invalid option selcted.')
				execute()
			except (NameError, SyntaxError):
				print('Invalid option selected.')
			except (TypeError):
				print('Exiting...')
				ssh.close()
				sys.exit(0)
	except paramiko.AuthenticationException:
		print('Authentication Failed: Please check username and password.')
	except paramiko.ssh_exception.NoValidConnectionsError:
		print('Connection Refused: Unable to connect to port 22 on ' + hostname)
else:
	print('' + hostname + ' is not pingable, please check network connectivity.')

sys.exit(0)
