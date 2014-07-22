#!/usr/bin/env python

import sys
from parseone import *
from parsetwo import *
from parsepexpect import *
from parsegcc import *
from parsellvm import *
import contextlib
import os
import argparse
import subprocess

repo_list=['aarch','2','3']
arch_list=['aarch64','2','3']
package_list=['gcc49','llvm','check','acl']
PROJECT="devel:arm_toolchain:Mobile:Base"
PROJECT_e=PROJECT.replace(":","\:")+"/"
repo=""
arch=""
package=""
debug = False

@contextlib.contextmanager
def cd(path):
   old_path = os.getcwd()
   os.chdir(path)
   try:
       yield
   finally:
       os.chdir(old_path)

class parsing_args:
	def __init__(self):
		pass
	def parse(self):
		global debug
		parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
						description='''
		Build utils, run tests and compare results

		Examples:
		  -b aarch aarch64 gcc49 -d
		  -r aarch aarch64 gcc49
		  -c gcc49 week ago
		  -c gcc49 31.06.14 14.06.15
		  -c gcc49 gcc48
		  -c gcc49 aarch64 i586
						''')
		group = parser.add_mutually_exclusive_group(required=True)
		group.add_argument('-b','--build', help='build <> <> <>',nargs='+')
		group.add_argument('-r','--runtests',help='run tests <> <> <>', nargs='+')
		group.add_argument('-c','--compare',help='compare <> <> <>', nargs='+')
		parser.add_argument('-d','--debug',help='debug', action='store_true')
		args = parser.parse_args()
		if args.debug:
			debug = True
			print "===Debug==="
	###Build
		### OSC build request
		if len(args.build) == 3:
			print '===Osc build request..==='
			repo=args.build[0]
			arch=args.build[1]
			package=args.build[2]
			if repo in repo_list and arch in arch_list and package in package_list: 
				print 'Good input'
				osc_build.checkout()
				osc_build.build()
			else:
				print 'Bad input'
				parser.print_help()
		else:
			parser.print_help()
		print args.build
		###
	###Run_tests
	

class build:
	def __init__(self):
		pass

class osc_build(build):
	def _init_(self):
		super(build, self).__init__()
	@staticmethod		
	def checkout():
		if os.path.exists(PROJECT+'/'+package):
			print "Package already exists"
			with cd(PROJECT+"/"+package):
				if not debug:
					print "Updating.."
					subprocess.call(["osc", "update"])
		else:
			print "===Checkout..==="
			subprocess.call(["osc", "checkout", PROJECT, package])
	def build():
	        with cd(PROJECT+"/"+package):
			print "===Building..==="
			subprocess.call(["osc", "build", repo, arch])

'''
one = parseone()
one.parse("./one.txt") 
one.show()

two = parsetwo()
two.parse("./gcc_res.txt")
two.show()

two1 = parsetwo()
two1.parse("./gcc_res1.txt")
two1.show()

pex = parsepexpect()
pex.parse("cat","./pex.txt")
pex.show()

print '===GCC RESULTS==='
gcc = parsegcc()
gcc.parse("./libstdc++.sum")
gcc.show()

print '===LLVM RESULTS==='
llvm = parsellvm()
llvm.parse("./gcc.sum")
llvm.show()
'''
parsing_args_inst=parsing_args()
parsing_args_inst.parse()

class main:
	def __init__(self):
		pass
	
print 'eof!'
