#!/usr/bin/env python

import sys
import contextlib
import os
import argparse
import subprocess
import re
import datetime
from pymongo import MongoClient
import time

argparser = None
args = None
# TODO expand this
repo_list = ['aarch','2','3']
arch_list = ['aarch64','2','3']
package_list = ['gcc49','llvm','check','acl']
##
PROJECT = "devel:arm_toolchain:Mobile:Base"
PROJECT_e = PROJECT.replace(":","\:")+"/"
repo = ""
arch = ""
package = ""
compiler = ""
version = ""
debug = False

@contextlib.contextmanager
def cd(path):
	old_path = os.getcwd()
        os.chdir(path)
        try:
                yield
        finally:
                os.chdir(old_path)

def RepresentsInt(s):
        try:
                int(s)
                return True
        except ValueError:
                return False

class Parsing_args(object):
	def __init__(self):
		pass
	## TODO parse expand
	# 
	#  Just edit description section and add some arguments to the parser 	
	def parse(self):
		global debug,argparser,args
		argparser = argparse.ArgumentParser(
			 formatter_class=argparse.RawDescriptionHelpFormatter,
			 description='''
		Build utils, run tests and compare results

		Examples:
		  -b osc 'aarch aarch64 gcc49 --no-verify --clean' -d 
		  -r osc 'aarcg aarch64 gcc49'
		  -c gcc49 week ago
		  -c gcc49 31.06.14 14.06.15
		  -c gcc49 gcc48
		  -c gcc49 aarch64 i586
		  -e my_collection 
		  -e 100500
						''')
		group = argparser.add_mutually_exclusive_group(required=True)
		group.add_argument('-b','--build', help="OSC co&build: -b osc 'REPOSITORY ARCH PACKAGE [OPTS]'\n",nargs='+')
		group.add_argument('-r','--runtests',help="Run tests: -r osc 'REPOSITORY ARCH PACKAGE'", nargs = '+') 
		group.add_argument('-p','--parse',help='Parsing results: -p PACKAGE')
		group.add_argument('-c','--compare',help='Compare results between A and B(time,repo,aarch,version): -c PACKAGE A B', nargs='+')
		argparser.add_argument('-d','--debug',help='debug', action='store_true')
		argparser.add_argument('-e','--erase',help='erase db COLLECTION/COUNT of the oldest documents')
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
	# add some NON osc build requests 
	@staticmethod
	def parse_args():
                ### OSC build request
		if args.build[0]=='osc':
		        print '===Osc build request..==='
			osc = Build_osc()
			osc.start()
		else:
			print 'Bad input'
			argparser.print_help()
			sys.exit(0)
		
		if debug:
			print 'build args:'
			print args.build

class Build_osc(object):
	params=""
	def __init__(self):
		global repo,arch,package
		self.params = args.build[1]
		mList = self.params.split(' ')
		if len(mList) >= 3:
			repo=mList[0]
			arch=mList[1]
			package=mList[2]
			del mList[2]
			self.params = ' '.join(mList)
		else:
			print 'Bad input'
			argparser.print_help()
			sys.exit(0)

	def start(self): 
		if repo in repo_list:
			if arch in arch_list:
				if package in package_list:
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
		if os.path.exists(PROJECT+'/'+package):
			print "Package already exists"
			with cd(PROJECT+"/"+package):
				if not debug:
					print "===Updating..==="
					subprocess.call(["osc", "update"])
		else:
			print "===Checkout..==="
			subprocess.call(["osc", "checkout", PROJECT, package])

	def build(self):
	        with cd(PROJECT+"/"+package):
			print "===Building..==="
			subprocess.call(["osc build " + self.params], shell = True)

class Run_tests(object):
	def __init__(self):
		global package
		package = args.runtests
        ## TODO tests expand
        #
        # add some NON osc run tests requests  	
        @staticmethod
        def parse_args():
		### OSC run tests request
		if args.runtests[0]=='osc':
                        print '===Osc run tests request..==='
                        osc = Run_tests_osc()
                        osc.start()
		else:
			print 'Bad input'
			argparser.print_help()
			sys.exit(0)

		if debug:
			print 'runtests args: '
			print args.runtests

class Run_tests_osc(object):
	params=""
	## TODO tests expand
        #
        # add new packages in the start method 
	def __init__(self):
        	global repo,arch,package
                self.params = args.runtests[1]
                mList = self.params.split(' ')
                if len(mList) >= 3:
                        repo=mList[0]
                        arch=mList[1]
                        package=mList[2]
                        del mList[2]
                        self.params = ' '.join(mList)
                else:
                        print 'Bad input'
			argparser.print_help()
                        sys.exit(0)
		
	def start(self):
		if repo in repo_list:
                        if arch in arch_list:
                                if package in package_list:
                                        print 'Good input'
					self.get_results()
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

	def get_results(self):
		global compiler,version
		if package == 'gcc49':
			print '===GCC 4.9 test request==='
			compiler = 'gcc'
			version = '4.9'
			db.add_textfile("/var/tmp/build-root/home/abuild/rpmbuild/BUILD/gcc-4.9.0/testresults/test_summary.txt")
		else:
			print 'No support for package ' + package
			print 'DIY: look at the class Run_tests_osc, method get_results'

class Parse(object):
	def __init__(self):
        	pass
	## TODO parse expand
	#
	#	
	@staticmethod
	def parse_args():
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
	
class Parse_gcc49(object):
	path="./testresults/test_summary.txt"
        pass_cnt = 0
        xpass_cnt = 0
        fail_cnt = 0
        xfail_cnt = 0
        unsupported_cnt= 0
        unresolved_cnt= 0
        def __init__(self):
                self.pass_cnt = 0
                self.xpass_cnt = 0
                self.fail_cnt = 0
                self.xfail_cnt = 0
                self.unsupported_cnt = 0
                self.unresolved_cnt = 0
	def start(self):
                pass_regexp = re.compile('(?:# of expected passes\s*)(\d+)')
                xpass_regexp = re.compile('(?:# of unexpected successes\s*)(\d+)')
                fail_regexp = re.compile('(?:# of expected failures\s*)(\d+)')
                xfail_regexp = re.compile('(?:# of unexpected failures\s*)(\d+)')
                unsupported_regexp = re.compile('(?:# of unsupported tests\s*)(\d+)')
                unresolved_regexp = re.compile('(?:# of unresolved testcases\s*)(\d+)')
                with open(self.path) as f:
                        for line in f:
                                if pass_regexp.match(line):
					self.pass_cnt += int(pass_regexp.match(line).group(1))
                                if fail_regexp.match(line):
                                        self.fail_cnt += int(fail_regexp.match(line).group(1)) 
                                if xpass_regexp.match(line):
                                        self.xpass_cnt += int(xpass_regexp.match(line).group(1))
                                if fail_regexp.match(line):
                                        self.xfail_cnt += int(fail_regexp.match(line).group(1))
                                if unsupported_regexp.match(line):
                                        self.unsupported_cnt += int(unsupported_regexp.match(line).group(1))
				if unresolved_regexp.match(line):
					self.unresolved_cnt += int(unresolved_regexp.match(line).group(1))
		self.show()
	
        def show(self):
		print '===GCC 4.9 TESTS RESULTS==='
                print 'PASS: %d' % self.pass_cnt
                print 'FAIL: %d' % self.fail_cnt
                print 'XPASS: %d' % self.xpass_cnt
                print 'XFAIL: %d' % self.xfail_cnt
                print 'UNSUPPORTED: %d' % self.unsupported_cnt
                print 'UNRESOLVED: %d' % self.unresolved_cnt

class MongoHQ(object):
	db = None
	def __init__(self):
		MONGO_URL = os.environ.get('MONGOHQ_URL')
		client = MongoClient(MONGO_URL)
		self.db = client.ssdb
				
	def collection_list(self):
		print "===Collection list==="
		return self.db.collection_names()
	
	def add_textfile(self,path):
		print '===Uploading log file to the database==='
		fname="filename"
		collection = self.db.kim_collection
		f = open(path)
		text = ""
		text = f.read()
		text_file_doc = {fname: path, "contents": text, "date": datetime.datetime.now().strftime('%d.%m.%Y'), "time": datetime.datetime.now().strftime('%H:%M:%S'), 'repo': repo, 'aarch': arch, 'package': package, 'compiler': compiler, 'version': version}
		collection.insert(text_file_doc)

	def operations(self):
		self.erase()
	def erase(self):
                if args.erase:
                        if RepresentsInt(args.erase):# and args.erase < db.users.count:
				#db.collection.remove()
                                pass # TODO erase COUNT of the oldest documents
				#for user in db.users.find().where('this.name == "user 2" || this.level>3'):
				#    print user
                        else:
				if args.erase in db.collection_list():
					print "Collection " + args.erase  + " will be deleted after 5 seconds..press Ctrl + C to interrupt"
					time.sleep(5)
					self.db.drop_collection(args.erase)
				else:
					print "Wrong collection"
				print db.collection_list()
		
class Compare(object):
        def __init__(self):
                pass
        ## TODO compare expand
        #
        #       
        @staticmethod
        def parse_args():
		global argparser,args
                if args.parse[0] == 'gcc49':
                        print '===GCC 4.9 compare request==='
                        compare_gcc49 = Compare_gcc49()
                        compare_gcc49.start()
			
                else:
                        print 'Bad input'
                        argparser.print_help()
                        sys.exit(0)

                if debug:
                        print 'compare agrs'
                        print args.compare
			
class Compare_gcc49(object):
        params=""
        def __init__(self): # TODO 
		mList=[]
                self.params = args.compare[1]
                if len(mList) >= 3:
                        repo=mList[0]
                        arch=mList[1]
                        package=mList[2]
                        del mList[2]
                        self.params = ' '.join(mList)
                else:
                        print 'Bad input'
			argparser.print_help()
                        sys.exit(0)
		
	def start(self):
		pass
		
Parsing_args_inst=Parsing_args()
Parsing_args_inst.parse()
db = MongoHQ()
db.operations()
if args.build:
	Build.parse_args()
if args.runtests:
	Run_tests.parse_args()
if args.parse:
	Parse.parse_args()	
if args.compare:
	Compare.parse_args()	
print '====finish==='
