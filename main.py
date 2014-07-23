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

argparser=None
args=None
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

class Parsing_args(object):
	def __init__(self):
		pass
	def parse(self):
		global debug,argparser,args
		argparser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
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
		group = argparser.add_mutually_exclusive_group(required=True)
		group.add_argument('-b','--build', help='build <> <> <>',nargs='+')
		group.add_argument('-r','--runtests',help='run tests <> <> <>') 
		group.add_argument('-c','--compare',help='compare <> <> <>', nargs='+')
		argparser.add_argument('-d','--debug',help='debug', action='store_true')
		### OSC build option
		argparser.add_argument('--no-verify',dest='build_options',action='append_const',const='--no-verify')
		argparser.add_argument('--clean',dest='build_options',action='append_const',const='--clean')
		###
		args = argparser.parse_args()
		if args.debug:
			debug = True
			print "===Debug==="
		if debug:print args

class Build(object):
	def __init__(self):
		pass
	@staticmethod
	def parse_args():
		global argparser,args
                ### OSC build request
		if len(args.build) == 3:
		        print '===Osc build request..==='
			Osc_build()
		else:
			argparser.print_help()

class Osc_build(Build):
	global repo,arch,package
	build_options=""
	def __init__(self):
		super(Build, self).__init__()
		self.repo=args.build[0]
		self.arch=args.build[1]
		self.package=args.build[2]
		if self.repo in repo_list and self.arch in arch_list and self.package in package_list:
			print 'Good input'
			self.checkout()
			if args.build_options:
				self.build_options=' '.join(args.build_options)
			if debug:print self.build_options 
			self.build()
		else:
			print 'Bad input'
			argparser.print_help()

	def checkout(self):
		if os.path.exists(PROJECT+'/'+self.package):
			print "Package already exists"
			with cd(PROJECT+"/"+self.package):
				if not debug:
					print "===Updating..==="
					subprocess.call(["osc", "update"])
		else:
			print "===Checkout..==="
			subprocess.call(["osc", "checkout", PROJECT, self.package])

	def build(self):
	        with cd(PROJECT+"/"+self.package):
			print "===Building..==="
			subprocess.call(["osc build " + " " + self.repo + " " + self.arch + " " + self.build_options], shell = True)

class Run_tests(object):
	def __init__(self):
		pass
        @staticmethod
        def parse_args():
		global argparser,args
		if args.runtests == 'gcc':
			print '===GCC49 test request==='
		else:
			print 'Bad input'
			argparser.print_help()

		print 'runtests args: '
		print args.runtests

class Run_tests_gcc49(Run_tests):
	def __init__(self):
		super(Run_tests_gcc49, self).__init__()
	@staticmethod
	def get_log():
		pass
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
Parsing_args_inst=Parsing_args()
Parsing_args_inst.parse()
if args.build:
	Build.parse_args()
if args.runtests:
	Run_tests.parse_args()
		
print '====finish==='
