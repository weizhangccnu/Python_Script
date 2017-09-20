#!/usr/bin/env python
# -*- co4ding:utf-8 -*-
import os
import sys
import time
import h5py
import socket
import ctypes
from ctypes import *
import subprocess
import numpy as np
#hostname = "192.168.2.3"               #wire network hostname
hostname = "192.168.1.116"               #wireless network hostname
port = 5025                             #host tcp port
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
##define a class for HDF5IO_waveform_event struct
#
class HDF5IO_waveform_event(Structure):
    _fields_ = [('eventId', c_ulong),
                ('wavBuf', c_char_p)]

#------------------------------------------------------------------------#
def query_data_from_scope(X_Range):
    ss.send(":ACQuire:SRATe:ANALog?;")          #Query sample rate
    Sample_Rate = float(ss.recv(128)[1:])   
    print "Sample rate:%.1f"%Sample_Rate
    total_point = Sample_Rate * X_Range
    print total_point

    ss.send(":SYSTem:HEADer OFF;")              #Query analog store depth
    ss.send(":WAVeform:SOURce CHANnel1;")       #Waveform source 
    ss.send(":WAVeform:BYTeorder LSBFirst;")    #Waveform data byte order
    ss.send(":WAVeform:FORMat WORD;")           #Waveform data format
    ss.send(":WAVeform:STReaming 1;")           #Waveform streaming on
    ss.send(":WAVeform:DATA? 1,%d;"%int(total_point))         #Query waveform data with start address and length
    n = total_point * 2 + 3
    print "n = %d"%n                            #calculate fetching data byte number
    totalContent = ""
    totalRecved = 0
    while totalRecved < n:                      #fetch data
        #print n, (n-totalRecved)
        onceContent = ss.recv(int(n - totalRecved))
        #print len(onceContent)
        totalContent += onceContent
        totalRecved = len(totalContent)
    length = len(totalContent)
    print length-3
    return [totalContent[3:length], length-3]

#note that: every command should be terminated with a semicolon
#------------------------------------------------------------------------#
## main function: sent oscilloscope commands and fetch data
#
def main():
    hdf5iodll = CDLL("./hdf5io.so")             #invoke hdf5io.c share object

    ss.send("*IDN?;")                           #read back device ID
    print "Instrument ID: %s"%ss.recv(128)   

    nEvents = int(sys.argv[1])                  #the first argumeent is nEvents 
    print "nEvents: %d"%nEvents 

    nWfmPerChunk = int(sys.argv[2])             #the second argument is nWfmPerChunk
    print "nWfmPerChunk: %d"%nWfmPerChunk

    nCh = int(sys.argv[3],16)                   #the third argument is nWfmPerChunk
    print "nCh: %d"%nCh
        
    chMask = 4                                  #chMask

    ss.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
    Sample_point = int(ss.recv(128)[1:]) - 3   
    nPt = Sample_point
    print "nPt: %d"%nPt
    
    nFrame = 0

    ss.send(":WAVeform:XRANge?;")               #Query X-axis range 
    X_Range = float(ss.recv(128)[1:])
    dt = X_Range

    ss.send(":TIMebase:POSition?;")             #Query X-axis timebase position 
    Timebase_Poistion = float(ss.recv(128)[1:])
    t0 = Timebase_Poistion
    print "t0:%.6f"%t0

    ss.send(":WAVeform:YRANge?;")               #Query Y-axis range
    Y_Range = float(ss.recv(128)[1:])   
    ymult = (Y_Range, 0.0, 0.0, 0.0)
    print ymult

    ss.send(":CHANnel1:OFFset?;")               #Channel1 Offset 
    CH1_Offset = float(ss.recv(128)[1:])   
    yoff = (CH1_Offset, 0.0, 0.0, 0.0)
    print yoff 
    
    yzero = (0.0, 0.0, 0.0, 0.0)
    
    ss.send(":TIMebase:POSition?;")             #Query X-axis timebase position 
    Timebase_Poistion = float(ss.recv(128)[1:])
    print "Timebase_Position:%.6f"%Timebase_Poistion

    ss.send(":WAVeform:XRANge?;")               #Query X-axis range 
    X_Range = float(ss.recv(128)[1:])
    print "XRange:%f"%X_Range

    ss.send(":WAVeform:YRANge?;")               #Query Y-axis range
    Y_Range = float(ss.recv(128)[1:])   
    print "YRange:%f"%Y_Range
    Y_Factor = Y_Range/62712.0

    hdf5iodll.HDF5IO_open_file.restype = POINTER(HDF5IO_waveform_file)
    hdf5iodll.HDF5IO_open_file.argtypes = [c_char_p, c_ulong, c_ulong]
    wavFile = hdf5iodll.HDF5IO_open_file("TMIIaCSAOut.h5", nWfmPerChunk, nCh) 
    print "wavFile->waveFid: %d"%wavFile.contents.waveFid
    print "wavFile->nPt: %d"%wavFile.contents.nPt
    print "wavFile->nCh: %d"%wavFile.contents.nCh
    print "wavFile->nWfmPerChunk: %d"%wavFile.contents.nWfmPerChunk
    print "wavFile->nEvent: %d"%wavFile.contents.nEvent

    wavAttr = pointer(waveform_attribute(chMask, 2*nPt, nFrame, dt, t0, ymult, yoff, yzero))
    hdf5iodll.HDF5IO_write_waveform_attribute_in_file_header.argtypes = [POINTER(HDF5IO_waveform_file), POINTER(waveform_attribute)]
    # specified the return type
    hdf5iodll.HDF5IO_read_waveform_attribute_in_file_header.restype = c_int
    ret = hdf5iodll.HDF5IO_write_waveform_attribute_in_file_header(wavFile, wavAttr)
    print "ret: %d"%ret
    print "wavAttr->chMask: %d"%wavAttr.contents.chMask
    print "wavAttr->nPt: %d"%wavAttr.contents.nPt
    print "wavAttr->nFrames: %d"%wavAttr.contents.nFrames
    print "wavAttr->dt: %f"%wavAttr.contents.dt
    print "wavAttr->t0: %f"%wavAttr.contents.t0
    print "wavAttr->ymult: %f %f %f %f"%(wavAttr.contents.ymult[0],wavAttr.contents.ymult[1],wavAttr.contents.ymult[2],wavAttr.contents.ymult[3])
    print "wavAttr->yoff: %f %f %f %f"%(wavAttr.contents.yoff[0],wavAttr.contents.yoff[1],wavAttr.contents.yoff[2],wavAttr.contents.yoff[3])
    print "wavAttr->yoff: %f %f %f %f"%(wavAttr.contents.yzero[0],wavAttr.contents.yzero[1],wavAttr.contents.yzero[2],wavAttr.contents.yzero[3])

    ## write dataset
    [scope_data, length] = query_data_from_scope(X_Range)
    print length    
    time.sleep(2)
    #print scope_data
    #buf3 = c_int * (length/2)
    #scope_dat = []
    #for i in xrange(length/2):              #store data into file
    #    print (ord(scope_data[i*2+1])<<8)+ord(scope_data[i*2])
    buf2 = c_char_p()
    buf2.value = ''
    for i in xrange(length):
        buf2.value += scope_data[i]
    #buf = c_char_p()
    #buf.value = 'a'*length 
    hdf5iodll.HDF5IO_write_event.argtypes = [POINTER(HDF5IO_waveform_file), POINTER(HDF5IO_waveform_event)]
    hdf5iodll.HDF5IO_write_event.restype = c_int
    #wavEvent = pointer(HDF5IO_waveform_event(0, buf))
    #ret = hdf5iodll.HDF5IO_write_event(wavFile, wavEvent)
    #print "ret: %d"%ret
    wavEvent = pointer(HDF5IO_waveform_event(0, buf2))
    ret = hdf5iodll.HDF5IO_write_event(wavFile, wavEvent)
    print "ret: %d"%ret

    ## flush hdf5 file
    hdf5iodll.HDF5IO_flush_file.argtypes = [POINTER(HDF5IO_waveform_file)]    
    hdf5iodll.HDF5IO_flush_file.restype = c_int
    ret = hdf5iodll.HDF5IO_flush_file(wavFile)
    print "ret: %d"%ret

    ## close hdf5 file
    hdf5iodll.HDF5IO_close_file.argtypes = [POINTER(HDF5IO_waveform_file)]
    hdf5iodll.HDF5IO_close_file.restype = c_int
    ret = hdf5iodll.HDF5IO_close_file(wavFile)
    print "ret: %d"%ret
    
    ##open file for read
    hdf5iodll.HDF5IO_open_file_for_read.argtypes = [c_char_p] 
    hdf5iodll.HDF5IO_open_file_for_read.restype = POINTER(HDF5IO_waveform_file) 
    wavFile = hdf5iodll.HDF5IO_open_file_for_read("TMIIaCSAOut.h5")
    print "HDF5IO(waveform_file)->waveFid:%d"%wavFile.contents.waveFid
    print "HDF5IO(waveform_file)->nPt:%d"%wavFile.contents.nPt
    print "HDF5IO(waveform_file)->nCh:%d"%wavFile.contents.nCh
    print "HDF5IO(waveform_file)->nWfmPerChunk:%d"%wavFile.contents.nWfmPerChunk
    print "HDF5IO(waveform_file)->nEvent:%d"%wavFile.contents.nEvent
    ## read waveform attribute
    wavAttr = pointer(waveform_attribute(0x0a, 10000, 100, 0.0001, 0.0, (1.1,1.2,1.3,1.4), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0)))
    hdf5iodll.HDF5IO_read_waveform_attribute_in_file_header.argtypes = [POINTER(HDF5IO_waveform_file), POINTER(waveform_attribute)]
    hdf5iodll.HDF5IO_read_waveform_attribute_in_file_header.restype = c_int 
    ret = hdf5iodll.HDF5IO_read_waveform_attribute_in_file_header(wavFile, wavAttr)
    print "ret: %d"%ret
    print "wavAttr->chMask: %d"%wavAttr.contents.chMask
    print "wavAttr->nPt: %d"%wavAttr.contents.nPt
    print "wavAttr->nFrames: %d"%wavAttr.contents.nFrames
    print "wavAttr->dt: %f"%wavAttr.contents.dt
    print "wavAttr->t0: %f"%wavAttr.contents.t0
    print "wavAttr->ymult: %f %f %f %f"%(wavAttr.contents.ymult[0],wavAttr.contents.ymult[1],wavAttr.contents.ymult[2],wavAttr.contents.ymult[3])
    print "wavAttr->yoff: %f %f %f %f"%(wavAttr.contents.yoff[0],wavAttr.contents.yoff[1],wavAttr.contents.yoff[2],wavAttr.contents.yoff[3])
    print "wavAttr->yzero: %f %f %f %f"%(wavAttr.contents.yzero[0],wavAttr.contents.yzero[1],wavAttr.contents.yzero[2],wavAttr.contents.yzero[3])

    buf2 = c_char_p()
    #buf2.value = '0'*100
    wavEvent = pointer(HDF5IO_waveform_event(0,buf2))
    hdf5iodll.HDF5IO_read_event.argtypes = [POINTER(HDF5IO_waveform_file), POINTER(HDF5IO_waveform_event)]
    hdf5iodll.HDF5IO_read_event.restype = c_int   
    ret = hdf5iodll.HDF5IO_read_event(wavFile, wavEvent)   
    print "ret: %d"%ret

    ## close hdf5 file
    hdf5iodll.HDF5IO_close_file.argtypes = [POINTER(HDF5IO_waveform_file)]
    hdf5iodll.HDF5IO_close_file.restype = c_int
    ret = hdf5iodll.HDF5IO_close_file(wavFile)
    print "ret: %d"%ret

    f = h5py.File('TMIIaCSAOut.h5','r')           #open .h5 file in read-only mode
    print f.attrs.keys()                                    #get the name of all attributes attached to root group object
    for attr in f.attrs:                                    #get each attributes values
        print attr,":",f.attrs[attr]
    print f.keys()                                          #acquire dataset info 
    data = f['C0'].value                            
    print data
    print len(data[0])
    for i in xrange(nPt):
        print ((data[0][i*2])<<8)+(data[0][i*2+1])
#========================================================#
## if statement
#
if __name__ == '__main__':
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
    ss.connect((hostname,port))                                 #connect to the server
    main()
