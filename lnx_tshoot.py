#!/usr/bin/env python
#Linux Troubleshooting script - run basic Linux commands via python script

# Modules
from __future__ import print_function
import argparse, paramiko, sys, getpass, subprocess

### for testing ###
hostname = '192.168.1.39'
username = 'root'
password = getpass.getpass('Please enter password: ')
command = 'uptime'
###################

# Global variables.
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Class for colors.

# Define a function for commands menu:
options = ['Check system uptime.', 'Check free memory.', 'Check if a process is running.',
	 'Check for a string in /var/log/messages.', 'EXIT']
def menu():
	print('Select from the following options [1-5]: ')
	for number,option in enumerate(options, 1):
		print(number, option)

# Define ssh & exec functions.
def connect():
	ssh.connect(hostname, port=22, username=username, password=password)

def execute():
	stdin,stdout,stderr = ssh.exec_command(command)
	type(stdin)
	print(stdout.read())

connect()
execute()
# Add options for hostname and username.
# raw_inputs for if no option is selected.
# getpass to enter password.

# if/else statement to ping the host
	# if pingable:
		# while loop to slected an option in menu and run the command.
			# if/else statement for choices.
	# else:
		# exit.
