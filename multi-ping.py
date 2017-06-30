#!/usr/bin/python

from __future__ import print_function
import os, sys, subprocess, argparse
#import sys
#import subprocess
#import argparse

class colors(object):
	Red = '\033[91m'
	Green = '\033[92m'
	Reset = '\033[0m'

parser = argparse.ArgumentParser(usage='multi-ping -f <file>')
required = parser.add_argument_group('required arguments')
required.add_argument('-f', '--file', help='specify the file with full path')
args = parser.parse_args()

if not args.file:
	print(colors.Red + 'Please select a file' + colors.Reset + '\n')
#	parser.print_help()
	sys.exit(1)

if os.path.isfile(args.file):
	print(colors.Green + args.file + ' is a valid file, proceeding...' + colors.Reset + '\n')
else:
	print(colors.Red + 'File not found. Please check filename and path, exiting...' + colors.Reset + '\n')
	sys.exit(1)

with open(args.file, 'r') as hosts:
	hostlist = [line.strip() for line in hosts]

for ip in hostlist:
	output = subprocess.Popen(['ping', '-c', '1', ip],stdout=subprocess.PIPE)
	stdout, stderr = output.communicate()

	if output.returncode == 0:
		print(colors.Green + ip + ' is pingable' + colors.Reset)
	else:
		print(colors.Red + ip + ' is NOT pingable' + colors.Reset)

print('\n')
sys.exit(0)
