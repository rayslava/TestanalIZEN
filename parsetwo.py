#!/usr/bin/env python

import os,sys,re

class parsetwo:
	result = []
	def __init__(self):
		self.result = []
	def parse(self, path):
		regex = re.compile(r"""
			(?:gcc_success\d*\s*:\s*)(?P<success>\d+)
			|(?:gcc_fail\d*\s*:\s*)(?P<fail> \d+)
			|(?:gcc_unapplicable\d*\s*:\s*)(?P<unapplicable> \d+)
			""", re.VERBOSE)
		with open(path) as f:
			for line in f:
				match = regex.search(line)
				if match:
					self.result.append([
						match.group('success'),
						match.group('fail'),
						match.group('unapplicable')
				])
				else:
					pass#print 'wtf'# Match attempt failed
	def show(self):
		print self.result
		#print self.result[0][0] + '<' + self.result[1][0]
		#print self.result[0][0]<self.result[1][0]

	
	
