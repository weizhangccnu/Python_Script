#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os 
import sys
import h5py
import time
"""@package h5py
This python file is used to test h5py package
"""
## @author WeiZhang
#================================================================#
def main():
    f = h5py.File('myfile.hdf5','w')
    print f.id
    print f.keys()
    grp = f.create_group("bar")
    print grp.name
    subgrp = grp.create_group("baz")
    print subgrp.name
    grp["name"] = 45
    out = grp["name"]
    print out
    for i in xrange(10):
        print i
    f.close()
#================================================================#
if __name__ == "__main__":
    sys.exit(main())
