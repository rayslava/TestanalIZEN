#!/usr/bin/env python

import sys
import contextlib
import os
import argparse
import subprocess
import re
from datetime import datetime, timedelta
from pymongo import MongoClient
import time
from osc import *
from parse import *
import h


def RepresentsInt(S):
        try:
                int(S)
                return True
        except ValueError:
                return False


class Parsing_args(object):
        ## TODO parse expand
        #
        #  Just edit description section and add some arguments to the parser
        def parse(self):
                h.argparser = argparse.ArgumentParser(
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description='''
                Build utils, run tests and compare results

                Examples:
                  -b osc 'aarch aarch64 gcc49 --no-verify --clean' -d
                  -r osc 'aarch aarch64 gcc49'
                  -c osc 'aarch aarch64 gcc49' 2 years ago
                  -c osc 'aarch aarch64 gcc49' week ago
                  -c osc 'aarch aarch64 gcc49' 31.06.14 14.06.15
                  -c osc 'aarch aarch64 gcc49' 31.06.14
                  -c osc 'aarch aarch64 gcc49' gcc48
                  -c osc 'aarch aarch64 gcc49' i586
                  -e my_collection
                  -e 100500
                                                ''')
                h.argparser.add_argument('-b', '--build', help="OSC co&build: "
                                       "-b osc 'REPOSITORY "
                                       "ARCH PACKAGE [OPTS]'",
                                       nargs='+')
                h.argparser.add_argument('-r', '--runtests',
                                       help="Run tests: "
                                       "-r osc 'REPOSITORY ARCH PACKAGE'",
                                       nargs='+')
                h.argparser.add_argument('-c', '--compare',
                                       help='Compare results between A and B'
                                       '(time,repo,aarch,version): '
                                       '-c PACKAGE A B',
                                       nargs='+')
                h.argparser.add_argument('-p', '--parse',
                                       help='Parsing results: -p PACKAGE')
                h.argparser.add_argument('-d', '--debug',
                                       help='debug',
                                       action='store_true')
                h.argparser.add_argument('-e', '--erase',
                                       help='erase db COLLECTION')
                h.args = h.argparser.parse_args()
                if h.args.debug:
                        h.debug = True
                        print "===Debug==="
                if h.debug:
                        print h.args


class Build(object):
        ## TODO build expand
        # Class chooses apropriate build type
        # add some NON osc build requests
        @staticmethod
        def parse_args():
                ### OSC build request
                if h.args.build[0] == 'osc':
                        print '===Osc build request..==='
                        osc = Build_osc()
                        osc.start()
                else:
                        print 'Bad input'
                        h.argparser.print_help()
                        sys.exit(0)

                if h.debug:
                        print 'build args:'
                        print h.args.build


class Run_tests(object):
        ## TODO tests expand
        # Class runs apropriate tests
        # add some NON osc run tests requests
        @staticmethod
        def parse_args():
                ### OSC run tests request
                if h.args.runtests[0] == 'osc':
                        print '===Osc run tests request..==='
                        osc = Run_tests_osc()
                        osc.start()
                else:
                        print 'Bad input'
                        h.argparser.print_help()
                        sys.exit(0)

                if h.debug:
                        print 'runtests args: '
                        print h.args.runtests


class Parse(object):
        def __init__(self):
                pass
        ## TODO parse expand
        # debug class
        #

        @staticmethod
        def parse_args():
                if h.args.parse == 'gcc':
                        print '===GCC parse request==='
                        # TODO
                else:
                        print 'Bad input'
                        h.argparser.print_help()
                        sys.exit(0)

                if h.debug:
                        print 'parse agrs'
                        print h.args.parse


class MongoHQ(object):
        ## TODO
        #
        #
        db = None

        def __init__(self):
                MONGO_URL = ('mongodb://'
                        'q9957789:qw12we23@kahana.mongohq.com:10013/ssdb')
                client = MongoClient(MONGO_URL)
                self.db = client.ssdb

        def collection_list(self):
                print "===Collection list==="
                return self.db.collection_names()

        def add_textfile(self, path, collection):
                print '===Uploading log file to the database==='
                collection = self.db[collection]
                f = open(path)
                text = ""
                text = f.read()
                text_file_doc = {"filename": path,
                                 "contents": text,
                                 "date": datetime.now(),
                                 'repo': h.repo,
                                 'aarch': h.arch,
                                 'package': h.package,
                                 'compiler': h.compiler,
                                 'version': h.version,
                                 'revision': h.revision}
                collection.insert(text_file_doc)
                if h.debug:  # shows last uploaded doc
                        print collection.find().sort('date', -1).limit(1)[0]

        def read_logs(self, collection, params=None):
                print '===Reading log files from the database==='
                collection = self.db[collection]
                logs = []
                log = []
                if params == None:
                        doc = collection.find().sort('date', -1).limit(1)[0]
                elif (type(params[0]) == datetime and
                        type(params[1] == datetime)):
                        start = params[0]
                        end = params[1]
                        count = collection.find({'date': {'$gte': start,
                                                          '$lt': end}}).count()
                        print str(count) + ' documents..'
                        i = 0
                        for doc in collection.find({'date': {'$gte': start,
                                                             '$lt': end}}):
                                log = []
                                contents = doc['contents']
                                contents = contents.decode("utf-8").split('\n')
                                log.append(contents)
                                log.append(doc['date'])
                                logs.append(log)
                return logs

        def operations(self):
                self.erase()

        def erase(self):
                if h.args.erase:
                        if RepresentsInt(h.args.erase):
                                pass
                        else:
                                if h.args.erase in db.collection_list():
                                        print ("Collection  %s"
                                                " will be deleted after "
                                                "5 seconds.."
                                                "press Ctrl + C to interrupt" %
                                                h.args.erase)
                                        time.sleep(5)
                                        self.db.drop_collection(h.args.erase)
                                else:
                                        print "Wrong collection"
                                print db.collection_list()


class Compare(object):
        ## TODO compare expand
        #
        #
        @staticmethod
        def parse_args():
                ### OSC compare request
                if h.args.compare[0] == 'osc':
                        print '===Osc compare request..==='
                        osc = Compare_osc()
                        osc.start()
                else:
                        print 'Bad input'
                        h.argparser.print_help()
                        sys.exit(0)

                if h.debug:
                        print 'compare args: '
                        print h.args.compare

if __name__ == "__main__":
        parsing_args = Parsing_args()
        parsing_args.parse()
        h.db = MongoHQ()
        h.db.operations()
        if h.args.build:
                Build.parse_args()
        if h.args.runtests:
                Run_tests.parse_args()
        if h.args.parse:
                Parse.parse_args()
        if h.args.compare:
                Compare.parse_args()
        print '====finish==='
