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
	## TODO parse expand
	# 
	#  Just edit description section and add some arguments to the parser 	
	def parse(self):
		global debug,argparser,args
		argparser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
						description='''
		Build utils, run tests and compare results

		Examples:
		  -b osc 'aarch aarch64 gcc49 --no-verify --clean' -d 
		  -r gcc49
		  -c gcc49 week ago
		  -c gcc49 31.06.14 14.06.15
		  -c gcc49 gcc48
		  -c gcc49 aarch64 i586
						''')
		group = argparser.add_mutually_exclusive_group(required=True)
		group.add_argument('-b','--build', help="OSC co&build: -b osc 'REPOSITORY ARCH PACKAGE [OPTS]'\n",nargs='+')
		group.add_argument('-r','--runtests',help='Run tests: -r PACKAGE') 
		group.add_argument('-p','--parse',help='Parsing results: -p PACKAGE')
		group.add_argument('-c','--compare',help='compare <> <> <>', nargs='+')
		argparser.add_argument('-d','--debug',help='debug', action='store_true')
		args = argparser.parse_args()
		if args.debug:
			debug = True
			print "===Debug==="
		if debug:print args

class Build(object):
	def __init__(self):
		pass
	## TODO build expand
	#
	#  
	@staticmethod
	def parse_args():
		global argparser,args
                ### OSC build request
		if args.build[0]=='osc':
		        print '===Osc build request..==='
			osc_build = Osc_build()
			osc_build.start()
		else:
			argparser.print_help()
			sys.exit(0)
		
		if debug:
			print 'build args:'
			print args.build

class Osc_build(Build):
	global repo,arch,package
	params=""
	def __init__(self):
		super(Build, self).__init__()
		self.params = args.build[1]
		mList = self.params.split(' ')
		if len(mList) >= 3:
			self.repo=mList[0]
			self.arch=mList[1]
			self.package=mList[2]
			del mList[2]
			self.params = ' '.join(mList)
		else:
			print 'Bad input'
			sys.exit(0)

	def start(self): 
		if self.repo in repo_list:
			if self.arch in arch_list:
				if self.package in package_list:
					print 'Good input'
					self.checkout()
					self.build()
				else: 
					print 'Wrong PACKAGE, package list:'
					print package_list
					argparser.print_help()
					sys.exit(0)
			else:
				print 'Wrong ARCH, arch list:'
				print arch_list
				argparser.print_help()
				sys.exit(0)
		else:
			print 'Wrong REPOSITORY, REPOSITORY list'
			print repo_list
			argparser.print_help()
			sys.exit(0)

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
			subprocess.call(["osc build " + self.params], shell = True)


class Run_tests(object):
	def __init__(self):
		pass
        ## TODO tests expand
        #
        #  	
        @staticmethod
        def parse_args():
		global argparser,args
		if args.runtests == 'gcc':
			print '===GCC 4.9 test request==='
			run_tests_gcc49 = Run_tests_gcc49()
			run_tests_gcc49.start()
		else:
			print 'Bad input'
			argparser.print_help()
			sys.exit(0)

		if debug:
			print 'runtests args: '
			print args.runtests

class Run_tests_gcc49(Run_tests):
	def __init__(self):
		super(Run_tests_gcc49, self).__init__()
	
	@staticmethod
	def start():
		pass # TODO

class Parse(object):
	def __init__(self):
        	pass
	## TODO parse expand
	#
	#	
	@staticmethod
	def parse_args():
		global argparser,args
		if args.parse == 'gcc49':
			print '===GCC 4.9 parse request==='
			parse_gcc49 = Parse_gcc49()
			parse_gcc49.start()
		else:
			print 'Bad input'
                        argparser.print_help()
                        sys.exit(0)

		if debug:
			print 'parse agrs'
			print args.parse
	
class Parse_gcc49(Parse):
	path="./libstdc++.sum"
        pass_cnt = 0
        xpass_cnt = 0
        fail_cnt = 0
        xfail_cnt = 0
        unsupported_cnt= 0
        error_cnt = 0
        warning_cnt = 0	
        def __init__(self):
                super(Parse_gcc49, self).__init__()
                self.pass_cnt = 0
                self.xpass_cnt = 0
                self.fail_cnt = 0
                self.xfail_cnt = 0
                self.unsupported_cnt= 0
                self.error_cnt = 0
                self.warning_cnt = 0
	def start(self):
                pass_regexp = re.compile('PASS\s*:\s*')
                xpass_regexp = re.compile('XPASS\s*:\s*')
                fail_regexp = re.compile('FAIL\s*:\s*')
                xfail_regexp = re.compile('XFAIL\s*:\s*')
                unsupported_regexp = re.compile('UNSUPPORTED\s*:\s*')
                error_regexp = re.compile('ERROR\s*:\s*')
                warning_regexp = re.compile('WARNING\s*:\s*')
                with open(self.path) as f:
                        for line in f:
                                if pass_regexp.match(line):
                                        self.pass_cnt += 1
                                if fail_regexp.match(line):
                                        self.fail_cnt += 1
                                if xpass_regexp.match(line):
                                        self.xpass_cnt += 1
                                if fail_regexp.match(line):
                                        self.xfail_cnt += 1
                                if unsupported_regexp.match(line):
                                        self.unsupported_cnt += 1
                                if error_regexp.match(line):
                                        self.error_cnt += 1
                                if warning_regexp.match(line):
                                        self.warning_cnt += 1
		self.show()
	
        def show(self):
		print '===GCC 4.9 TESTS RESULTS==='
                print 'PASS: %d' % self.pass_cnt
                print 'FAIL: %d' % self.fail_cnt
                print 'XPASS: %d' % self.xpass_cnt
                print 'XFAIL: %d' % self.xfail_cnt
                print 'UNSUPPORTED: %d' % self.unsupported_cnt
                print 'ERROR: %d' % self.error_cnt
                print 'WARNING: %d' % self.warning_cnt

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
if args.parse:
	Parse.parse_args()	

print '====finish==='
