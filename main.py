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

args = None
argparser = None
debug = False


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
                global debug, argparser, args
                argparser = argparse.ArgumentParser(
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
                argparser.add_argument('-b', '--build', help="OSC co&build: "
                                       "-b osc 'REPOSITORY "
                                       "ARCH PACKAGE [OPTS]'",
                                       nargs='+')
                argparser.add_argument('-r', '--runtests',
                                       help="Run tests: "
                                       "-r osc 'REPOSITORY ARCH PACKAGE'",
                                       nargs='+')
                argparser.add_argument('-c', '--compare',
                                       help='Compare results between A and B'
                                       '(time,repo,aarch,version): '
                                       '-c PACKAGE A B',
                                       nargs='+')
                argparser.add_argument('-p', '--parse',
                                       help='Parsing results: -p PACKAGE')
                argparser.add_argument('-d', '--debug',
                                       help='debug',
                                       action='store_true')
                argparser.add_argument('-e', '--erase',
                                       help='erase db COLLECTION')
                args = argparser.parse_args()
                if args.debug:
                        debug = True
                        print "===Debug==="
                if debug:
                        print args


class Build(object):
        ## TODO build expand
        # Class chooses apropriate build type
        # add some NON osc build requests
        @staticmethod
        def parse_args(args):
                ### OSC build request
                if args.build[0] == 'osc':
                        print '===Osc build request..==='
                        osc = Build_osc(args, db)
                        osc.start()
                else:
                        print 'Bad input'
                        print 'Please read help'
                        sys.exit(0)

                if debug:
                        print 'build args:'
                        print args.build


class Run_tests(object):
        ## TODO tests expand
        # Class runs apropriate tests
        # add some NON osc run tests requests
        @staticmethod
        def parse_args(args):
                ### OSC run tests request
                if args.runtests[0] == 'osc':
                        print '===Osc run tests request..==='
                        osc = Run_tests_osc(args, db)
                        osc.start()
                else:
                        print 'Bad input'
                        print 'Please read help'
                        sys.exit(0)

                if debug:
                        print 'runtests args: '
                        print args.runtests


class Parse(object):
        def __init__(self):
                pass
        ## TODO parse expand
        # debug class
        #

        @staticmethod
        def parse_args(args):
                if args.parse == 'gcc':
                        print '===GCC parse request==='
                        # TODO
                else:
                        print 'Bad input'
                        print 'Please read help'
                        sys.exit(0)

                if args.debug:
                        print 'parse agrs'
                        print args.parse


class MongoHQ(object):
        ## TODO
        #
        #
        db = None

        def __init__(self):
                MONGO_URL = os.environ.get('MONGOHQ_URL')
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
                                 'repo': repo,
                                 'aarch': arch,
                                 'package': package,
                                 'compiler': compiler,
                                 'version': version}
                collection.insert(text_file_doc)
                if debug:  # shows last uploaded doc
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
                if args.erase:
                        if RepresentsInt(args.erase):
                                pass
                        else:
                                if args.erase in db.collection_list():
                                        print ("Collection  %s"
                                                " will be deleted after "
                                                "5 seconds.."
                                                "press Ctrl + C to interrupt" %
                                                args.erase)
                                        time.sleep(5)
                                        self.db.drop_collection(args.erase)
                                else:
                                        print "Wrong collection"
                                print db.collection_list()


class Compare(object):
        ## TODO compare expand
        #
        #
        @staticmethod
        def parse_args(args):
                ### OSC compare request
                if args.compare[0] == 'osc':
                        print '===Osc compare request..==='
                        osc = Compare_osc(args, db)
                        osc.start()
                else:
                        print 'Bad input'
                        print 'Please read help'
                        sys.exit(0)

                if debug:
                        print 'compare args: '
                        print args.compare

if __name__ == "__main__":
        parsing_args = Parsing_args()
        parsing_args.parse()
        db = MongoHQ()
        db.operations()
        if args.build:
                Build.parse_args(args)
        if args.runtests:
                Run_tests.parse_args(args)
        if args.parse:
                Parse.parse_args(args)
        if args.compare:
                Compare.parse_args(args)
        print '====finish==='
