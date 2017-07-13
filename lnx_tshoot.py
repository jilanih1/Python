#!/usr/bin/env python
#Linux Troubleshooting script - run basic Linux commands via python script

# Modules
from __future__ import print_function
import argparse, paramiko, sys, getpass, subprocess, os, time

#For paramiko (ssh/missing keys)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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
	selct = colors.blu + 'Select an option [1-10] or type "exit": ' + colors.rst
	sping = colors.ylw + ' is pingable, continuing...' + colors.rst
	fping = colors.ylw + ' is not pingable, please check network connectivity.' + colors.rst
	prcin = colors.red + 'Please enter process: ' + colors.rst
	varin = colors.red + 'Please enter string to search: ' + colors.rst
	trcin = colors.red + 'Please enter address to trace: ' + colors.rst
	invld = colors.ylw + 'Invalid option selected. Please choose from the following:' + colors.rst
	extng = colors.ylw + 'Thank you for using LNX_Tshoot!' + '\n' + 'Exiting...' + colors.rst
	autfl = colors.ylw + 'Authentication Failed: Please check username and password.' + colors.rst
	confl = colors.ylw + 'Connection Refused: Unable to connect to port 22 on ' + colors.rst
	sshfl = colors.ylw + 'SSH session was terminated unexpectedly.' + colors.rst

class commands():
	sysi = 'dmidecode -t system' #Needs root access on remote host.
	lnxk = 'uname -srv' #Kernel -s = name, -r = release, -v = version.
	osvr = 'cat /etc/*-release | head -n1' #'head -n1' shows only the first line.
	uptm = 'uptime'
	free = 'free -h' #-h for human-readable.
	dfsk = 'df -h'
	neti = 'ifconfig' #shows only interfaces currently in use.
	proc = 'ps -ef | grep -v grep | grep -i ' #'grep -v grep' ommits grep process from output.
	varm = 'cat /var/log/messages | grep -i '
	trcr = 'traceroute ' #May take a long time (and fail) for external addresses (due to firewalls).

#Defines functions to call menu, clear screen & exit:
options = ['Show System Information.', 'Show Linux Kernel Version.', 'Show OS Version.', 'Show System Uptime.', 
	'Show Memory Usage.', 'Show Filesystems.', 'Show Network Interfaces.', 'Check Process:', 
	'Check for a string in /var/log/messages:', 'Trace Address:']
def menu():
	time.sleep(.5)
	print(colors.blu + '-' * 45)
	for number,option in enumerate(options, 1):
		print(number, option)
	print('-' * 45 + colors.rst)

def clear():
	os.system('clear')

def close():
	print(messages.extng)
	time.sleep(.5)
	ssh.close()
	sys.exit()

#Defines main function:
#If host is pingable, tries to connect to host. Displays the menu.
#Lets the user choose a command to run.
#If the incorrect password is entered or sshd service is not running paramiko throws
# exceptions and error messages are displayed.
def main():
	clear()
	pinghost = subprocess.Popen(['ping', '-c', '3', hostname],stdout=subprocess.PIPE)
	stdout, stderr = pinghost.communicate()
	if pinghost.returncode == 0:
		print(colors.red + hostname + messages.sping)
		try:
			ssh.connect(hostname, port=22, username=username, password=password)
			while True:
				menu()
				try:
					choice = int(input(messages.selct))
					if choice == 1:
						command = commands.sysi
					elif choice == 2:
						command = commands.lnxk
					elif choice == 3:
						command = commands.osvr
					elif choice == 4:
						command = commands.uptm
					elif choice == 5:
						command = commands.free
					elif choice == 6:
						command = commands.dfsk
					elif choice == 7:
						command = commands.neti
					elif choice == 8:
						var = raw_input(messages.prcin)
						command = commands.proc + var
					elif choice == 9:
						var = raw_input(messages.varin)
						command = commands.varm + var
					elif choice == 10:
						var = raw_input(messages.trcin)
						command = commands.trcr + var
					else:
						clear()
						command = null
						print(messages.invld)
					clear()
					print(colors.red + 'Linux Command: ' + colors.blu + command + colors.rst)
					try: #if ssh session from remote node is terminated while script is running.
						stdin,stdout,stderr = ssh.exec_command(command)
						type(stdin)
					except (paramiko.ssh_exception.SSHException):
						print(messages.sshfl)
						close()
					print(colors.cyn + stdout.read()[:-1] + colors.rst) #[:-1]del extra line.
				except (NameError, SyntaxError):
					clear()
					print(messages.invld)
				except (TypeError):
					clear()
					close()
		except (paramiko.AuthenticationException):
			print(messages.autfl)
		except (paramiko.ssh_exception.NoValidConnectionsError):
			print(messages.confl + colors.red + hostname + colors.rst)
	else:
		print(colors.red + hostname + messages.fping)

#Allows script to be run with hostname and username options:
parser = argparse.ArgumentParser(usage='lnx_tshoot.py -s <hostname> -u <username>')
parser.add_argument('-s', '--hostname', help='Specify hostname to ssh into.')
parser.add_argument('-u', '--username', help='Enter username.')
args = parser.parse_args()

#If no option is selected for hostname and username, allows it to be entered via input:
if not args.hostname:
	hostname = raw_input(messages.nohst)
else:
	hostname = args.hostname
if not args.username:
	username = raw_input(messages.nousr)
else:
	username = args.username

#Hides password input:
password = getpass.getpass(colors.blu + '' + username + '@' + hostname + ' password: ' + colors.rst)

if __name__ == '__main__':
	main()
close()
