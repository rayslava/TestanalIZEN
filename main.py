#!/usr/bin/env python

import sys, sh
from parseone import *
from parsetwo import *
from parsepexpect import *
from parsegcc import *
from parsellvm import *
from sh import osc
import argparse

def parsing_args():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
					description='''
	Build utils, run tests and compare results

	Examples:
	  -b aarch aarch64 gcc49 
	  -r aarch aarch64 gcc49
	  -c gcc49 week ago
	  -c gcc49 31.06.14 14.06.15
	  -c gcc49 gcc48
	  -c gcc49 aarch64 i586
					''')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-b','--build', help='build <> <> <>',required=False, nargs='+')
	group.add_argument('-r','--runtests',help='run tests <> <> <>', required=False, nargs='+')
	group.add_argument('-c','--compare',help='compare <> <> <>', required=False, nargs='+')
	args = parser.parse_args()

	print args.build
	###

print "===TestanalIZEN==="

one = parseone()
one.parse("./one.txt") 
one.show()

two = parsetwo()
two.parse("./gcc_res.txt")
two.show()

two1 = parsetwo()
two1.parse("./gcc_res1.txt")
two1.show()

pex = parsepexpect()
pex.parse("cat","./pex.txt")
pex.show()

print '===GCC RESULTS==='
gcc = parsegcc()
gcc.parse("./libstdc++.sum")
gcc.show()

print '===LLVM RESULTS==='
llvm = parsellvm()
llvm.parse("./gcc.sum")
llvm.show()

parsing_args();

class main:
	def __init__(self):
		pass
	
print 'eof!'
