#!/usr/bin/env python

from datetime import datetime,timedelta
from parse import * 
import contextlib
import sys

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

@contextlib.contextmanager 
def cd(path): 
        old_path = os.getcwd() 
        os.chdir(path) 
        try: 
                yield 
        finally: 
                os.chdir(old_path) 

class OSC(object):
        ## 
        # Parent class, parses osc params 
        # 
        params = ""
	db = None
        def __init__(self, args, db):
                global repo,arch,package
                if args.build and len(args.build) >= 2:
                        self.params = args.build[1]
                elif args.runtests:
                        self.params = args.runtests[1]
                elif args.compare:
                        self.params = args.compare[1]
                mList = self.params.split(' ')
                if len(mList) >= 3:
                        repo=mList[0]
                        arch=mList[1]
                        package=mList[2]
                        del mList[2]
                        self.params = ' '.join(mList)
                else:
                        print 'Bad input'
                        print 'Please read help'
                        sys.exit(0)
		self.db = db
		self.args = args

class Build_osc(OSC):
        ##
        # Class checkout and build osc package
        # TODO check repo, arch and package lists
        def start(self):
                if repo in repo_list:
                        if arch in arch_list:
                                if package in package_list:
                                        if(self.args.debug): print 'Good input'
                                        self.checkout()
                                        self.build()
                                else:
                                        print 'Wrong PACKAGE, package list:'
                                        print package_list
                                        print 'Please read help'
                                        sys.exit(0)
                        else:
                                print 'Wrong ARCH, arch list:'
                                print arch_list
                                print 'Please read help'
                                sys.exit(0)
                else:
                        print 'Wrong REPOSITORY, REPOSITORY list'
                        print repo_list
                        print 'Please read help'
                        sys.exit(0)
        def checkout(self):
                if os.path.exists(PROJECT+'/'+package):
                        print "Package already exists"
                        with cd(PROJECT+"/"+package):
                                if not self.args.debug:
                                        print "===Updating..==="
                                        subprocess.call(["osc", "update"])
                else:
                        print "===Checkout..==="
                        subprocess.call(["osc", "checkout", PROJECT, package])

        def build(self):
                with cd(PROJECT+"/"+package):
                        print "===Building..==="
                        subprocess.call(["osc build " + self.params], shell = True)

class Run_tests_osc(OSC):
        ## TODO tests expand
        # Class get osc test results
        # add new packages in the start method 
        def start(self):
                if repo in repo_list:
                        if arch in arch_list:
                                if package in package_list:
                                        if(self.args.debug): print 'Good input'
                                        self.get_results()
                                else:
                                        print 'Wrong PACKAGE, package list:'
                                        print package_list
                                        print 'Please read help'
                                        sys.exit(0)
                        else:
                                print 'Wrong ARCH, arch list:'
                                print arch_list
                                print 'Please read help'
                                sys.exit(0)
                else:
                        print 'Wrong REPOSITORY, REPOSITORY list'
                        print repo_list
                        print 'Please read help'
                        sys.exit(0)

        def get_results(self):
                global compiler,version
                if package == 'gcc49':
                        print '===GCC 4.9 test request==='
                        compiler = 'gcc'
                        version = '4.9'
                        self.db.add_textfile("/var/tmp/build-root/home/abuild/rpmbuild/BUILD/gcc-4.9.0/testresults/test_summary.txt", compiler)
                else:
                        print 'No support for package ' + package
                        print 'DIY: look at the class Run_tests_osc, method get_results'

class Compare_osc(OSC):
        ## TODO compare expand
        #
        # add new packages in the start method 
        A = None
        B = None
        date1 = None
        date2 = None
        def __init__(self, args, db):
                super(Compare_osc, self).__init__(args, db)
                self.A = None
                self.B = None
                self.date1 = datetime.now()
                self.date2 = datetime.now()
                if len(args.compare) >= 5:
                        if args.compare[4] == "ago": # ex: -c osc 'aarch..' 2 years ago
                                dt = timedelta()
                                if args.compare[3] == 'years':
                                        dt = timedelta(days=366*int(args.compare[2]))
                                elif args.compare[3] == 'months':
                                        dt = timedelta(days=31*int(args.compare[2]))
                                elif  args.compare[3] == 'weeks':
                                        dt = timedelta(weeks=int(args.compare[2]))
                                elif  args.compare[3] == 'days':
                                        dt = timedelta(days=int(args.compare[2]))
                                elif  args.compare[3] == 'hours':
                                        dt = timedelta(hours=int(args.compare[2]))
                                elif  args.compare[3] == 'minutes':
                                        dt = timedelta(minutes=int(args.compare[2]))
                                else:
                                        print 'Bad input'
                                        print 'Please read help'
                                        sys.exit(0)
                                self.date1 = datetime.now() - dt
                        else:
                                print 'Bad input'
                                print 'Please read help'
                                sys.exit(0)
                elif len(args.compare) >= 4:
                        if args.compare[3] == "ago": # ex: -c osc 'aarch..' week ago    
                                dt = 0
                                if args.compare[2] == 'year':
                                        dt = timedelta(days=366)
                                if args.compare[2] == 'month':
                                        dt = timedelta(days=31)
                                if  args.compare[2] == 'week':
                                        dt = timedelta(weeks=1)
                                if  args.compare[2] == 'day':
                                        dt = timedelta(days=1)
                                elif  args.compare[2] == 'hour':
                                        dt = timedelta(hours = 1)
				else:
                                        print 'Bad input'
                                        print 'Please read help'
                                        sys.exit(0)
                                self.date1 = datetime.now() - dt
                        else: # ex: -c osc 'aarch..' 12.12.12 21.12.21
                                self.date1 = self.parse_datetime(args.compare[2])
                                self.date2 = self.parse_datetime(args.compare[3])

                elif len(args.compare)>= 3:
                        if args.compare[2] in arch_list:
                                pass
                        elif args.compare[2] in package_list:
                                pass
                        else: # ex: -c osc 'aarch..' 12.12.12
                                self.date1 = self.parse_datetime(args.compare[2])

        def parse_datetime(self, date):
                try:
                        return datetime.strptime(date, '%d.%m.%y')
                except ValueError:
                        print 'Bad input'
                        print 'Please read help'
                        sys.exit(0)

        def start(self):
                logs = self.db.read_logs('gcc',[self.date1, self.date2]) # TODO package
                for log in logs:
                        parse_gcc = Parse_gcc(log)
                        parse_gcc.start()
