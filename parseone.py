#!/usr/bin/env python

import os,sys,re

class parseone:
	result = []
	def __init__(self):
		self.result = []
	def parse(self, path):
		regex = re.compile(r"""
			(?:res\d*\s*=\s*)(?P<res>\d+)
			|(?:other\d*\s*=\s*)(?P<other> \d+)
			""", re.VERBOSE|re.IGNORECASE)
		with open(path) as f:
			for line in f:
				match = regex.search(line)
				if match:
					self.result.append([
						match.group('res'),
						match.group('other')
				])
				else:
					pass#print 'wtf'# Match attempt failed
	def show(self):
		print self.result
		#print self.result[0][0] + '<' + self.result[1][0]
		#print self.result[0][0]<self.result[1][0]

	
	
