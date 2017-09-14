#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ctypes
from ctypes import *
import numpy as np
from mpi4py import MPI
import sys
import os
import time
import h5py
#------------------------------------------------------------------------#
##define a class
#
class StructPointer(Structure):
    pass

#------------------------------------------------------------------------#
## compare .dat format file with .h5 format file
#
def compare():
    fname = h5py.File('output_data.h5','w')
    dset = fname.create_dataset("MyDataset", (10000000,), 'i', compression='gzip', compression_opts=9)
    dset[:] = np.arange(10000000)
    attr = (1, 2, 3)
    dset.attrs.create("waveform_attributes", attr)
    dset.attrs.create("waveform_number", 12)
    print dset.shape
    print dset.attrs.keys()
    print dset.len()
    with open("./output_data.dat",'w') as outfile:
        for i in xrange(10000000):
            outfile.write("%d\n"%i) 
#------------------------------------------------------------------------#
def main():
    hdf5iodll = cdll.LoadLibrary("./hdf5io.so")
    #compare() 
    StructPointer._fields_ = [('x', c_int),('y',c_int),('next', POINTER(StructPointer))]
    hdf5iodll.test.restype = POINTER(StructPointer)
    p = hdf5iodll.test()
    print p.contents.y
    print "Ok!"
#------------------------------------------------------------------------#
if __name__ == "__main__":
    main()

