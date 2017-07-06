#!/usr/bin/env python
#Linux Troubleshooting script - run basic Linux commands via python script

# Modules
from __future__ import print_function
import argparse, paramiko, sys, getpass, subprocess

# Global variables.
# paramiko

# Class for colors.

# Define a function for commands menu:
options = ['Check system uptime.', 'Check free memory.', 'Check if a process is running.',
	 'Check for a string in /var/log/messages.', 'EXIT']
def menu():
	print('Select from the following options [1-5]: ')
	for number,option in enumerate(options, 1):
		print(number, option)
menu()

# Define ssh function.

# Add options for hostname and username.
# raw_inputs for if no option is selected.
# getpass to enter password.

# if/else statement to ping the host
	# if pingable:
		# while loop to slected an option in menu and run the command.
			# if/else statement for choices.
	# else:
		# exit.
