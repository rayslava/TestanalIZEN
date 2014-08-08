#!/usr/bin/env python

import re
import sys
import random
from threading import Thread
import pexpect
import h


class Parse(object):
        contents = None
        date = None
        result = None

        def __init__(self, log=[[], []]):
                self.result = None
                self.contents = log[0]
                self.date = log[1]

        def start(self):
                pass

        def show(self):
                pass

        def get(self):
                return self.result


class Parse_pexpect(Parse):
        def __init__(self):
                super(Parse_pexpect, self).__init__()

        def before(self, cmd, expect, regex, group=0):
                child = pexpect.spawn(cmd)
                child.expect(expect)
                string = child.before
                if (h.debug):
                        print string
                regex = re.compile(regex)
                match = regex.search(string)
                if match:
                        if (h.debug):
                                print match.group(group)
                        self.result = match.group(group)
                else:
                        pass  # print 'wtf'# Match attempt failed

        def show(self):
                print self.result


class Parse_gcc(Thread, Parse):
        pass_cnt = 0
        xpass_cnt = 0
        fail_cnt = 0
        xfail_cnt = 0
        unsupported_cnt = 0
        unresolved_cnt = 0
        contents = ""

        def __init__(self, log):
                Thread.__init__(self)
                self.pass_cnt = 0
                self.xpass_cnt = 0
                self.fail_cnt = 0
                self.xfail_cnt = 0
                self.unsupported_cnt = 0
                self.unresolved_cnt = 0
                self.contents = log[0]
                self.date = log[1]

        def run(self):
                pass_regexp = re.compile('(?:# of expected passes\s*)(\d+)')
                xpass_regexp = re.compile('(?:# of unexpected successes\s*)'
                                          '(\d+)')
                fail_regexp = re.compile('(?:# of expected failures\s*)(\d+)')
                xfail_regexp = re.compile('(?:# of unexpected failures\s*)'
                                          '(\d+)')
                unsupported_regexp = re.compile('(?:# of unsupported tests\s*)'
                                                '(\d+)')
                unresolved_regexp = re.compile('(?:# of unresolved '
                                               'testcases\s*)(\d+)')
                for line in self.contents:
                        if pass_regexp.match(line):
                                self.pass_cnt +=\
                                        int(pass_regexp.match(line).group(1))
                        if fail_regexp.match(line):
                                self.fail_cnt +=\
                                        int(fail_regexp.match(line).group(1))
                        if xpass_regexp.match(line):
                                self.xpass_cnt +=\
                                        int(xpass_regexp.match(line).group(1))
                        if fail_regexp.match(line):
                                self.xfail_cnt +=\
                                        int(fail_regexp.match(line).group(1))
                        if unsupported_regexp.match(line):
                                self.unsupported_cnt +=\
                                        int(unsupported_regexp
                                                .match(line)
                                                .group(1))
                        if unresolved_regexp.match(line):
                                self.unresolved_cnt +=\
                                        int(unresolved_regexp
                                                .match(line)
                                                .group(1))
                self.rand()  # TODO debug function, remove before release

        def show(self):
                print '===GCC TESTS RESULTS==='
                print self.date
                print 'PASS: %d' % self.pass_cnt
                print 'FAIL: %d' % self.fail_cnt
                print 'XPASS: %d' % self.xpass_cnt
                print 'XFAIL: %d' % self.xfail_cnt
                print 'UNSUPPORTED: %d' % self.unsupported_cnt
                print 'UNRESOLVED: %d' % self.unresolved_cnt

        def get(self):
                return [self.pass_cnt,
                        self.fail_cnt,
                        self.xpass_cnt,
                        self.xfail_cnt,
                        self.unsupported_cnt,
                        self.unresolved_cnt]

        def rand(self):
                self.pass_cnt += random.gauss(0, self.pass_cnt / 10)
                self.fail_cnt += random.gauss(0, self.fail_cnt / 10)
                self.xfail_cnt += random.gauss(0, self.xfail_cnt / 10)
                self.xpass_cnt += random.gauss(0, self.xpass_cnt / 10)
                self.unsupported_cnt += random.gauss(0,
                                                     self.unsupported_cnt / 10)
                self.unresolved_cnt += random.gauss(0,
                                                     self.unresolved_cnt / 10)
