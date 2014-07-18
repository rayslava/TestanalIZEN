#!/usr/bin/env python

import os,sys,re
import pexpect

class parsepexpect:
	result = []
	def __init__(self):
		self.result = []

	def parse(self, cmd, path):
		string = ""
		child = pexpect.spawn (cmd + ' ' + path)
		#===
                child.expect ('\d+\r\n')
                print 'before\r\n' + child.before
                print 'after\r\n' + child.after
		string = child.before + " = " + child.after
		print string
		#===
		regex = re.compile(r"""
			(?:value\d*\s*=\s*)(?P<value>\d+)
			""", re.VERBOSE)
		match = regex.search(string)
		if match:
			self.result.append([
				match.group('value')
		])
		else:
			pass#print 'wtf'# Match attempt failed

	def show(self):
		print self.result
		#print self.result[0][0] + '<' + self.result[1][0]
		#print self.result[0][0]<self.result[1][0]
