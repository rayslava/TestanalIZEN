#!/usr/bin/env python

from parseone import *
from parsetwo import *
from parsepexpect import *
from parsegcc import *
from parsellvm import *

print '===TestanalIZEN==='

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
