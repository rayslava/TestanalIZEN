#!/usr/bin/env python

import re
import sys

class Parse_gcc(object):
        ## TODO
        # 
        #    
        pass_cnt = 0
        xpass_cnt = 0
        fail_cnt = 0
        xfail_cnt = 0
        unsupported_cnt= 0
        unresolved_cnt= 0
        log = None
        def __init__(self,log):
                self.pass_cnt = 0
                self.xpass_cnt = 0
                self.fail_cnt = 0
                self.xfail_cnt = 0
                self.unsupported_cnt = 0
                self.unresolved_cnt = 0
                self.log = log

        def start(self):
                pass_regexp = re.compile('(?:# of expected passes\s*)(\d+)')
                xpass_regexp = re.compile('(?:# of unexpected successes\s*)(\d+)')
                fail_regexp = re.compile('(?:# of expected failures\s*)(\d+)')
                xfail_regexp = re.compile('(?:# of unexpected failures\s*)(\d+)')
                unsupported_regexp = re.compile('(?:# of unsupported tests\s*)(\d+)')
                unresolved_regexp = re.compile('(?:# of unresolved testcases\s*)(\d+)')
                for line in self.log:
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
                print '===GCC TESTS RESULTS==='
                print 'PASS: %d' % self.pass_cnt
                print 'FAIL: %d' % self.fail_cnt
                print 'XPASS: %d' % self.xpass_cnt
                print 'XFAIL: %d' % self.xfail_cnt
                print 'UNSUPPORTED: %d' % self.unsupported_cnt
                print 'UNRESOLVED: %d' % self.unresolved_cnt

