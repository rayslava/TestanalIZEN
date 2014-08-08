#!/usr/bin/env python

from datetime import datetime, timedelta
from parse import *
import contextlib
import sys
import matplotlib.pyplot as plt
import os
import subprocess
import h


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

        def __init__(self):
                if h.args.build and len(h.args.build) >= 2:
                        self.params = h.args.build[1]
                elif h.args.runtests:
                        self.params = h.args.runtests[1]
                elif h.args.compare:
                        self.params = h.args.compare[1]
                mList = self.params.split(' ')
                if len(mList) >= 3:
                        h.repo = mList[0]
                        h.arch = mList[1]
                        h.package = mList[2]
                        del mList[2]
                        self.params = ' '.join(mList)
                else:
                        print 'Bad input'
                        h.argparser.print_help()
                        sys.exit(0)


class Build_osc(OSC):
        ##
        # Class checkout and build osc package
        # TODO check repo, arch and package lists
        def start(self):
                if h.repo in h.repo_list:
                        if h.arch in h.arch_list:
                                if h.package in h.package_list:
                                        if h.debug:
                                                print 'Good input'
                                        self.checkout()
                                        self.build()
                                else:
                                        print 'Wrong PACKAGE, package list:'
                                        print h.package_list
                                        h.argparser.print_help()
                                        sys.exit(0)
                        else:
                                print 'Wrong ARCH, arch list:'
                                print h.arch_list
                                h.argparser.print_help()
                                sys.exit(0)
                else:
                        print 'Wrong REPOSITORY, REPOSITORY list'
                        print h.repo_list
                        h.argparser.print_help()
                        sys.exit(0)

        def checkout(self):
                if os.path.exists(h.PROJECT + '/' + h.package):
                        print "Package already exists"
                        with cd(h.PROJECT + "/" + h.package):
                                if not h.debug:
                                        print "===Updating..==="
                                        subprocess.call(["osc", "update"])
                else:
                        print "===Checkout..==="
                        subprocess.call(["osc",
                                        "checkout",
                                        h.PROJECT,
                                        h.package])

        def build(self):
                with cd(h.PROJECT + "/" + h.package):
                        print "===Revision==="
                        parse_pexpect = Parse_pexpect()
                        parse_pexpect.start("osc update",
                                                "At revision \d+",
                                                'after',
                                                "\d+")
                        h.revision = parse_pexpect.get()
                        print h.revision
                        print "===Building..==="
                        subprocess.call(["osc build " + self.params],
                                        shell=True)


class Run_tests_osc(OSC):
        ## TODO tests expand
        # Class get osc test results
        # add new packages in the start method
        def start(self):
                if h.repo in h.repo_list:
                        if h.arch in h.arch_list:
                                if h.package in h.package_list:
                                        if(h.debug):
                                                print 'Good input'
                                        self.get_results()
                                else:
                                        print 'Wrong PACKAGE, package list:'
                                        print h.package_list
                                        h.argparser.print_help()
                                        sys.exit(0)
                        else:
                                print 'Wrong ARCH, arch list:'
                                print h.arch_list
                                h.argparser.print_help()
                                sys.exit(0)
                else:
                        print 'Wrong REPOSITORY, REPOSITORY list'
                        print h.repo_list
                        h.argparser.print_help()
                        sys.exit(0)

        def get_results(self):
                if h.package == 'gcc49':
                        print '===GCC 4.9 test request==='
                        h.compiler = 'gcc'
                        h.version = '4.9'
                        h.db.add_textfile("/var/tmp/build-root/home/abuild"
                                                "/rpmbuild/BUILD/gcc-4.9.0"
                                                "/testresults"
                                                "/test_summary.txt",
                                                h.compiler)
                else:
                        print 'No support for package ' + h.package
                        print ('DIY: look at the class Run_tests_osc, '
                               'method get_results')


class Compare_osc(OSC):
        ## TODO compare expand
        #
        # add new packages in the start method
        A = None
        B = None
        date1 = None
        date2 = None
        dates = []
        compare_type = None

        def __init__(self):
                super(Compare_osc, self).__init__()
                self.A = None
                self.B = None
                self.date1 = datetime.now()
                self.date2 = datetime.now()
                if len(h.args.compare) >= 5:
                        if h.args.compare[4] == "ago":
                        # ex: -c osc 'aarch..' 2 years ago
                                self.compare_type = 'datetime'
                                dt = timedelta()
                                if h.args.compare[3] == 'years':
                                        dt = timedelta(
                                                days=366 *
                                                int(h.args.compare[2]))
                                elif h.args.compare[3] == 'months':
                                        dt = timedelta(
                                                days=31 * int(h.
                                                                args.
                                                                compare[2]))
                                elif  h.args.compare[3] == 'weeks':
                                        dt = timedelta(
                                                weeks=int(h.args.compare[2]))
                                elif  h.args.compare[3] == 'days':
                                        dt = timedelta(
                                                days=int(h.args.compare[2]))
                                elif  h.args.compare[3] == 'hours':
                                        dt = timedelta(
                                                hours=int(h.args.compare[2]))
                                elif  h.args.compare[3] == 'minutes':
                                        dt = timedelta(
                                                minutes=int(h.args.compare[2]))
                                else:
                                        print 'Bad input'
                                        h.argparser.print_help()
                                        sys.exit(0)
                                self.date1 = datetime.now() - dt
                        else:
                                print 'Bad input'
                                h.argparser.print_help()
                                sys.exit(0)
                elif len(h.args.compare) >= 4:
                        if h.args.compare[3] == "ago":
                        # ex: -c osc 'aarch..' week ago
                                self.compare_type = 'datetime'
                                dt = 0
                                if h.args.compare[2] == 'year':
                                        dt = timedelta(days=366)
                                elif h.args.compare[2] == 'month':
                                        dt = timedelta(days=31)
                                elif  h.args.compare[2] == 'week':
                                        dt = timedelta(weeks=1)
                                elif  h.args.compare[2] == 'day':
                                        dt = timedelta(days=1)
                                elif  h.args.compare[2] == 'hour':
                                        dt = timedelta(hours=1)
                                else:
                                        print 'Bad input'
                                        h.argparser.print_help()
                                        sys.exit(0)
                                self.date1 = datetime.now() - dt
                        else:  # ex: -c osc 'aarch..' 12.12.12 21.12.21
                                self.compare_type = 'datetime'
                                self.date1 = self.parse_datetime(
                                        h.args.compare[2])
                                self.date2 = self.parse_datetime(
                                        h.args.compare[3])

                elif len(h.args.compare) >= 3:
                        if h.args.compare[2] in h.arch_list:
                                pass
                        elif h.args.compare[2] in h.package_list:
                                pass
                        else:  # ex: -c osc 'aarch..' 12.12.12
                                self.compare_type = 'datetime'
                                self.date1 = self.parse_datetime(
                                        h.args.compare[2])

        def parse_datetime(self, date):
                try:
                        return datetime.strptime(date, '%d.%m.%y')
                except ValueError:
                        print 'Bad input'
                        h.argparser.print_help()
                        sys.exit(0)

        def start(self):
                passfail_mass = []
                parse_gcc_list = []
                if self.compare_type == 'datetime':
                        # TODO compiller
                        logs = h.db.read_logs(h.compiler, [self.date1,
                                                        self.date2])
                        for log in logs:
                                passfail = []
                                self.dates.append(log[1])
                                parse_gcc = Parse_gcc(log)
                                parse_gcc.start()
                                parse_gcc_list.append(parse_gcc)
                        for parse_gcc in parse_gcc_list:
                                parse_gcc.join()
                                parse_gcc.show()
                                passfail = parse_gcc.get()
                                passfail_mass.append(passfail)
                        for i in range(len(passfail)):
                                y = []
                                for _ in range(len(passfail_mass)):
                                        y.append(passfail_mass[_][i])
                                self.plot_datetime(self.dates, y)

        def plot_datetime(self, x, y):
                plt.plot_date(x, y, fmt="r-")
                plt.gcf().autofmt_xdate()
                plt.show()
