#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ctypes
from ctypes import *
import numpy as np
from mpi4py import MPI
import sys
import os
import h5py
import time
'''
HDF5 datatype --------------> C datatype --------------> ctypes datatype --------------> N bytes
size_t                         long unsigned int            c_ulong                         8 
hid_t                          signed int                   c_int                           4 
unsigned int                   unsigned int                 c_uint                          4 
N/A                            double                       c_double                        8
N/A                            char *                       c_char_p                        8
''' 
#------------------------------------------------------------------------#
##define a class for StructPointer struct
#
class StructPointer(Structure):
    _fields_ = [('x', c_int),
                ('y',c_int)]
 
#------------------------------------------------------------------------#
##define a class for HDF5IO_waveform_file struct
#
class HDF5IO_waveform_file(Structure):
    _fields_ = [('waveFid', c_int),         #hid_t should be singed int type
                ('nPt', c_ulong), 
                ('nCh', c_ulong), 
                ('nWfmPerChunk', c_ulong), 
                ('nEvent', c_ulong)]

#------------------------------------------------------------------------#
##define a class for waveform_attribute struct
#
class waveform_attribute(Structure):
    _fields_ = [('chMask', c_uint), 
                ('nPt', c_ulong), 
                ('nFrames', c_ulong), 
                ('dt', c_double), 
                ('t0', c_double), 
                ('ymult', c_double*4), 
                ('yoff', c_double*4), 
                ('yzero', c_double*4)]

#------------------------------------------------------------------------#
##define a class for waveform_attribute struct
#
class HDF5IO_waveform_event(Structure):
    _fields_ = [('eventId', c_ulong),
                ('wavBuf', c_char_p)]

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
    #hdf5iodll.test.restype = POINTER(StructPointer)
    #p = hdf5iodll.test(49,4)
    #print p.contents.x
    #print p.contents.y

    # specified the return types by setting the restype, by default functions are assumed to return the C int type. 
    hdf5iodll.HDF5IO_open_file_for_read.restype = POINTER(HDF5IO_waveform_file) 
    wavFile = hdf5iodll.HDF5IO_open_file_for_read("TMS1mmSingleCSAOut1_1.h5")
    print "HDF5IO(waveform_file)->waveFid:%d"%wavFile.contents.waveFid
    print "HDF5IO(waveform_file)->nPt:%d"%wavFile.contents.nPt
    print "HDF5IO(waveform_file)->nCh:%d"%wavFile.contents.nCh
    print "HDF5IO(waveform_file)->nWfmPerChunk:%d"%wavFile.contents.nWfmPerChunk
    print "HDF5IO(waveform_file)->nEvent:%d"%wavFile.contents.nEvent

    ## read attributes from hdf5 file
    #define a waveform_attribute struct
    wavAttr = pointer(waveform_attribute(0x0a, 10000, 100, 0.0001, 0.0, (1.1,1.2,1.3,1.4), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0)))
    # specified the arguements of HDF5IO_read_waveform_attribute_in_file_header
    # POINTER: define a pointer variable do not need parameters 
    # pointer: define a pointer variable need parameters 
    hdf5iodll.HDF5IO_read_waveform_attribute_in_file_header.argtypes = [POINTER(HDF5IO_waveform_file), POINTER(waveform_attribute)]
    # specified the return type
    hdf5iodll.HDF5IO_read_waveform_attribute_in_file_header.restype = c_int 
    ret = hdf5iodll.HDF5IO_read_waveform_attribute_in_file_header(wavFile, wavAttr)
    print "ret: %d"%ret
    print "wavAttr->chMask: %d"%wavAttr.contents.chMask
    print "wavAttr->nFrames: %d"%wavAttr.contents.nFrames
    print "wavAttr->dt: %f"%wavAttr.contents.dt
    print "wavAttr->t0: %f"%wavAttr.contents.t0
    print "wavAttr->ymult: %f %f %f %f"%(wavAttr.contents.ymult[0],wavAttr.contents.ymult[1],wavAttr.contents.ymult[2],wavAttr.contents.ymult[3])
    print "wavAttr->yoff: %f %f %f %f"%(wavAttr.contents.yoff[0],wavAttr.contents.yoff[1],wavAttr.contents.yoff[2],wavAttr.contents.yoff[3])
    print "wavAttr->yoff: %f %f %f %f"%(wavAttr.contents.yzero[0],wavAttr.contents.yzero[1],wavAttr.contents.yzero[2],wavAttr.contents.yzero[3])


    ## read dataset 
    buf = c_char_p()
    wavEvent = pointer(HDF5IO_waveform_event(1, buf))
    print "wavEvent->eventId: %d"%wavEvent.contents.eventId
    print "wavEvent->wavBuf: %s"%wavEvent.contents.wavBuf
    hdf5iodll.HDF5IO_read_event.argtypes = [POINTER(HDF5IO_waveform_file), POINTER(HDF5IO_waveform_event)]
    hdf5iodll.HDF5IO_read_event.restype = c_int   
    ret = hdf5iodll.HDF5IO_read_event(wavFile, wavEvent)   
    print "ret: %d"%ret

    ## close hdf5 file
    hdf5iodll.HDF5IO_close_file.argtypes = [POINTER(HDF5IO_waveform_file)]
    hdf5iodll.HDF5IO_close_file.restype = c_int 
    ret = hdf5iodll.HDF5IO_close_file(wavFile)
    print "ret: %d"%ret
#------------------------------------------------------------------------#
if __name__ == "__main__":
    main()
