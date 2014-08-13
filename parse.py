#!/usr/bin/env python2

import re
import random
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

        def start(self, cmd, expect, part, regex, group=0):
                child = pexpect.spawn(cmd)
                child.expect(expect)
                if part is 'before':
                        string = child.before
                else:
                        string = child.after
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


class Parse_gcc(Parse):
        def __init__(self, log):
                #Thread.__init__(self)
                super(Parse_gcc, self).__init__(log)
                self.pass_cnt = 0
                self.xpass_cnt = 0
                self.fail_cnt = 0
                self.xfail_cnt = 0
                self.unsupported_cnt = 0
                self.unresolved_cnt = 0
                self.result = [self.pass_cnt,
                                self.fail_cnt,
                                self.xpass_cnt,
                                self.xfail_cnt,
                                self.unsupported_cnt,
                                self.unresolved_cnt]

        def start(self):
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
                regexps = [pass_regexp,
                        fail_regexp,
                        xpass_regexp,
                        xfail_regexp,
                        unsupported_regexp,
                        unresolved_regexp]
                for line in self.contents:
                        for i in range(len(regexps)):
                                if regexps[i].match(line):
                                        self.result[i] +=\
                                                int(regexps[i]
                                                        .match(line)
                                                        .group(1)
                                                )
                self.rand()  # TODO debug function, remove before release

        def show(self):
                print '===GCC TESTS RESULTS==='
                print self.date
                label = ['PASS:',
                        'FAIL:',
                        'XPASS:',
                        'XFAIL:',
                        'UNSUPPORTED:',
                        'UNRESOLVED:']
                for i in range(len(self.result)):
                        print '%s %d' % (label[i], self.result[i])

        def rand(self):
                for i in range(len(self.result)):
                        self.result[i] += random.gauss(0,
                                                        self.result[i] / 10)
