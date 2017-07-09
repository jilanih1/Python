#!/usr/bin/env python
#Linux Troubleshooting script - run basic Linux commands via python script

# Modules
from __future__ import print_function
import argparse, paramiko, sys, getpass, subprocess

#Classes for colors, messages and commands
class colors():
	red = '\033[91m'
	blu = '\033[94m'
	cyn = '\033[96m'
	ylw = '\033[93m'
	rst = '\033[0m'

class messages():
	nohst = colors.blu + 'no hostname specified, please enter hostname: ' + colors.rst
	nousr = colors.blu + 'no username specified, please enter username: ' + colors.rst
	selct = colors.blu + 'Select an option [1-4] or type "exit": ' + colors.rst
	sping = colors.ylw + ' is pingable, continuing...' + colors.rst
	fping = colors.ylw + ' is not pingable, please check network connectivity.' + colors.rst
	prcin = colors.blu + 'Please enter process: ' + colors.rst
	varin = colors.blu + 'Please enter string to search: ' + colors.rst
	invld = colors.red + 'Invalid option selected.' + colors.rst
	extng = colors.ylw + 'Exiting...' + colors.rst
	autfl = colors.ylw + 'Authentication Failed: Please check username and password.' + colors.rst
	confl = colors.ylw + 'Connection Refused: Unable to connect to port 22 on ' + colors.rst

class commands():
	uptm = 'uptime'
	free = 'free'
	proc = 'ps -ef | grep -v grep | grep -i '
	varm = 'cat /var/log/messages | grep -i '

#Defines functions to call menu, execute the code, and exit script:
options = ['Check system uptime.', 'Check free memory.', 'Check if a process is running.',
	 'Check for a string in /var/log/messages.']
def menu():
	print(colors.blu + '-' * 46)
	for number,option in enumerate(options, 1):
		print(number, option)
	print('-' * 46 + colors.rst)

def execute():
	print(colors.blu + command + colors.rst)
	stdin,stdout,stderr = ssh.exec_command(command)
	type(stdin)
	print(colors.cyn + stdout.read() + colors.rst)

def close():
	print(messages.extng)
	ssh.close()
	sys.exit()

#Allows script to be run with hostname and username options:
parser = argparse.ArgumentParser(usage='lnx_tshoot.py -s <hostname> -u <username>')
parser.add_argument('-s', '--hostname', help='Specify hostname to ssh into.')
parser.add_argument('-u', '--username', help='Enter username.')
args = parser.parse_args()

#If no option is selected for hostname and username, allows it to be entered:
if not args.hostname:
	hostname = raw_input(messages.nohst)
else:
	hostname = args.hostname
if not args.username:
	username = raw_input(messages.nousr)
else:
	username = args.username

#Hides password entry:
password = getpass.getpass(colors.blu + '' + username + '@' + hostname + ' password: ' + colors.rst)

#For paramiko (ssh/missing keys)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#If host is pingable, tries to connect to host. Displays the menu.
#Lets the user choose a command to run.
#If the incorrect password is entered or sshd service is not running paramiko throws
# exceptions and error messages is displayed.
pinghost = subprocess.Popen(['ping', '-c', '1', hostname],stdout=subprocess.PIPE)
stdout, stderr = pinghost.communicate()
if pinghost.returncode == 0:
	print(colors.red +  hostname + messages.sping)
	try:
		ssh.connect(hostname, port=22, username=username, password=password)
		while True:
			menu()
			try:
				choice = int(input(messages.selct))
				if choice == 1:
					command = commands.uptm
				elif choice == 2:
					command = commands.free
				elif choice == 3:
					var = raw_input(messages.prcin)
					command = commands.proc + var
				elif choice == 4:
					var = raw_input(messages.varin)
					command = commands.varm + var
				else:
					command = null
					print(messages.invld)
				execute()
			except (NameError, SyntaxError):
				print(messages.invld)
			except (TypeError):
				close()
	except paramiko.AuthenticationException:
		print(messages.autfl)
	except paramiko.ssh_exception.NoValidConnectionsError:
		print(messages.confl + colors.red + hostname + colors.rst)
else:
	print(colors.red + hostname + messages.fping)

close()
