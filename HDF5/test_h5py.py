#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os 
import sys
import h5py
import time
import numpy as np
"""@package h5py
This python file is used to test h5py package
"""
## @author WeiZhang
#================================================================#
def main():
    f = h5py.File('myfile.hdf5','w')
    dataset = f.create_dataset("DS1", (3200,6400), 'i', chunks=(4,8), compression='gzip', compression_opts=9) 
    data = np.zeros((3200,6400))
    print data
    for i in xrange(3200):
        for j in xrange(6400):
            data[i][j] = i*j-j
    print data
    time.sleep(1)
    dataset[...] = data
    print dataset[0:4]

    #group = f.create_group("somegroup")
    #f['alias'] = h5py.SoftLink('/somegroup')
    #print f['alias']

    #dset = f.create_dataset("default", (100,))
    #print dset

    #arr = np.arange(100)
    #print arr
    #dset = f.create_dataset("init", data=arr)
    #print dset
    #
    #dset = f.create_dataset("chunked", (100,100), chunks=(100, 100))
    #print dset
    #
    #dset = f.create_dataset("autochunk", (10,10), chunks=True)
    #print dset, dset.shape
    #result = dset[1:6,[1,3,8]]
    #print result.shape 

    #print f.id
    #print f.keys()
    #grp = f.create_group("bar")
    #print grp.name
    #subgrp = grp.create_group("baz")
    #print subgrp.name
    #grp["name"] = 45
    #out = grp["name"]
    #print out
    #myds = subgrp["MyDs"]
    #print myds
    #missing = subgrp["missing"]
    #print missing
    for i in xrange(2):
        print i
    f.close()
#================================================================#
if __name__ == "__main__":
    sys.exit(main())
