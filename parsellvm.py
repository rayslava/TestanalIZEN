#!/usr/bin/env python

import re

class parsellvm:
	pass_cnt = 0
	xpass_cnt = 0
	fail_cnt = 0
	xfail_cnt = 0
	unsupported_cnt= 0
	unresolved_cnt = 0
	def __init__(self):
		self.pass_cnt = 0
		self.xpass_cnt = 0
		self.fail_cnt = 0
		self.xfail_cnt = 0
		self.unsupported_cnt= 0
		self.unresolved_cnt= 0
	def parse(self, path):
		pass_regexp = re.compile('PASS\s*:\s*')
		xpass_regexp = re.compile('XPASS\s*:\s*')
		fail_regexp = re.compile('FAIL\s*:\s*')
		xfail_regexp = re.compile('XFAIL\s*:\s*')
		unsupported_regexp = re.compile('UNSUPPORTED\s*:\s*')
		unresolved_regexp= re.compile('UNRESOLVED\s*:\s*')
		with open(path) as f:
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
				if unresolved_regexp.match(line):
                                        self.unresolved_cnt += 1
	def show(self):
		print 'PASS: %d' % self.pass_cnt
		print 'FAIL: %d' % self.fail_cnt
		print 'XPASS: %d' % self.xpass_cnt
                print 'XFAIL: %d' % self.xfail_cnt
		print 'UNSUPPORTED: %d' % self.unsupported_cnt
		print 'UNRESOLVED: %d' % self.unresolved_cnt
