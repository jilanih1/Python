#!/usr/bin/env python

from __future__ import print_function
import os, sys, subprocess, argparse

class colors():
	Red = '\033[91m'
	Green = '\033[92m'
	Reset = '\033[0m'

class info():
	nofile = 'Please select a file'
	vafile = ' is a valid file, proceeding...'
	fafile = 'File not found. Please check filename and path, exiting...'
	success = ' is pingable'
	fail = ' is not pingable'
 
parser = argparse.ArgumentParser(usage='multi-ping -f <file>')
required = parser.add_argument_group('required arguments')
required.add_argument('-f', '--file', help='specify the file with full path')
args = parser.parse_args()

if not args.file:
	print(colors.Red + info.nofile + colors.Reset + '\n')
	sys.exit(1)

if os.path.isfile(args.file):
	print(colors.Green + args.file + info.vafile + colors.Reset + '\n')
else:
	print(colors.Red + info.fafile + colors.Reset + '\n')
	sys.exit(1)

with open(args.file, 'r') as hosts:
	hostlist = [line.strip() for line in hosts]
hosts.close()

for ip in hostlist:
	output = subprocess.Popen(['ping', '-c', '1', ip],stdout=subprocess.PIPE)
	stdout, stderr = output.communicate()

	if output.returncode == 0:
		print(colors.Green + ip + info.success + colors.Reset)
	else:
		print(colors.Red + ip + info.fail + colors.Reset)

print('\n')
sys.exit(0)
