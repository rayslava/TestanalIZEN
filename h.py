#!/usr/bin/env python

args = None
argparser = None
debug = False
db = None
# TODO expand this
repo_list = ['aarch', '2', '3']
arch_list = ['aarch64', 'i586', '3']
package_list = ['gcc49', 'llvm', 'check', 'acl', 'glibc']
##
PROJECT = "devel:arm_toolchain:Mobile:Base"
PROJECT_LIST = ['devel:arm_toolchain:Mobile:llvm',
                'devel:arm_toolchain:Mobile:Base']
repo = ""
arch = ""
package = ""
compiler = ""
version = ""
revision = ""
