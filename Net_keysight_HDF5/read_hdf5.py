#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ctypes
from ctypes import *
import numpy as np
from mpi4py import MPI
import sys
import os
import time
'''
C datatype --------------> ctypes datatype
size_t                      c_long
hid_t                       c_int
'''
#------------------------------------------------------------------------#
##define a class
#
class StructPointer(Structure):
    pass
#------------------------------------------------------------------------#
##define a class
#
class HDF5IO_waveform_file(Structure):
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
    #hdf5iodll = cdll.LoadLibrary("./hdf5io.so")        #the first method to invoke dll library on Linux
    hdf5iodll = CDLL("./hdf5io.so")                     #the second method to invoke dll library on Linux 
    #compare() 
    StructPointer._fields_ = [('x', c_long),('y',c_int),('next', POINTER(StructPointer))]
    hdf5iodll.test.restype = POINTER(StructPointer)
    p = hdf5iodll.test(49,2)
    print p.contents.x
    print p.contents.y

    HDF5IO_waveform_file._fields_ = [('waveFid', c_int), ('nPt', c_long), ('nCh', c_long), ('nWfmPerChunk', c_long), ('nEvent', c_long), ('next', POINTER(HDF5IO_waveform_file))]
    hdf5iodll.HDF5IO_open_file.restype = POINTER(HDF5IO_waveform_file)
    p = hdf5iodll.HDF5IO_open_file("TMS1mmSingleCSAOut1_1.h5", 100, 1)
    print p.contents.waveFid
    print p.contents.nPt
    print p.contents.nCh
    print p.contents.nWfmPerChunk
    print p.contents.nEvent

    q = create_string_buffer("Hello", 10)
    print sizeof(q), repr(q.raw)
    print "Ok!"
#------------------------------------------------------------------------#
if __name__ == "__main__":
    main()

