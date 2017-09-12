#!/usr/bin/env python
# -*- co4ding:utf-8 -*-
import os
import sys
import time
import h5py
import socket
import subprocess
import numpy as np
#hostname = "192.168.2.3"               #wire network hostname
hostname = "10.146.110.53"               #wireless network hostname
port = 5025                             #host tcp port
#note that: every command should be terminated with a semicolon
#========================================================#
## main function: sent oscilloscope commands and fetch data
#
def main():
    with open("./data_output.dat",'w') as outfile:
        ss.send("*IDN?;")                           #read back device ID
        print "Instrument ID: %s"%ss.recv(128)   

        #dt = h5py.special_dtype(enum = (np.dtype('int32'), np.dtype('array')))
        #print h5py.check_dtype(enum=dt)
        ## create a TMIIa_CSAOut.h5 file with write and read method
        filename = h5py.File('TMIIa_CSAOut.h5','a') #Read/Write if file exist; otherwise create
        nEvents = int(sys.argv[1])                  #the first argumeent is nEvents 
        print "nEvents: %d"%nEvents 
        filename.attrs.create("nEvents", nEvents)

        nWfmPerChunk = int(sys.argv[2])             #the second argument is nWfmPerChunk
        print "nWfmPerChunk: %d"%nWfmPerChunk
        filename.attrs.create("nWfmPerChunk", nWfmPerChunk)

        nCh = int(sys.argv[3],16)                   #the third argument is nWfmPerChunk
        print "nCh: %d"%nCh
        filename.attrs.create("nCh", nCh)
            
        chMask = 4                                  #chMask

        ss.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
        Sample_point = int(ss.recv(128)[1:]) - 3   
        nPt = Sample_point
        
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
        Ymult = [Y_Range, 0.0, 0.0, 0.0]
        print Ymult

        ss.send(":CHANnel1:OFFset?;")               #Channel1 Offset 
        CH1_Offset = float(ss.recv(128)[1:])   
        Yoff = [CH1_Offset, 0.0, 0.0, 0.0]
        print Yoff 
        
        Yzero = [0, 0, 0, 0]

        Waveform_Attributes = (chMask, nPt, nFrame, dt, t0, Ymult, Yoff, Yzero)
        #Waveform_Attributes = (chMask, nPt, nFrame, dt, t0)
        print Waveform_Attributes

        filename.attrs.create("Waveform Attributes", Waveform_Attributes, shape = None, dtype = object)
        for attr in filename.attrs:                 #get each attributes values
            print attr,":",filename.attrs[attr]

        ss.send(":TIMebase:POSition?;")             #Query X-axis timebase position 
        Timebase_Poistion = float(ss.recv(128)[1:])
        print "Timebase_Position:%.6f"%Timebase_Poistion

        ss.send(":WAVeform:XRANge?;")               #Query X-axis range 
        X_Range = float(ss.recv(128)[1:])
        print "XRange:%f"%X_Range

        ss.send(":WAVeform:YRANge?;")               #Query Y-axis range
        Y_Range = float(ss.recv(128)[1:])   
        print "YRange:%f"%Y_Range
        #Y_Factor = Y_Range/980.0
        Y_Factor = Y_Range/62712.0
        #print Y_Factor

        ss.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
        Sample_point = int(ss.recv(128)[1:]) - 3   
        nPt = Sample_point
        print "Sample Point:%d"%Sample_point
        
        ss.send(":WAVeform:XUNits?;")               #Query X-axis unit 
        print "X-axis Unit:%s"%(ss.recv(128)[1:])   

        ss.send(":WAVeform:YUNits?;")               #Query Y-axis unit 
        print "Y-axis Unit:%s"%(ss.recv(128)[1:])   

        ss.send(":CHANnel1:OFFset?;")               #Channel1 Offset 
        CH1_Offset = float(ss.recv(128)[1:])   
        print "Channel 1 Offset:%f"%CH1_Offset
        print "X_Range:%f"%X_Range 
        if X_Range >= 2.0:
            Xrange = np.arange(-X_Range/2.0,X_Range/2.0,X_Range*1.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion
        elif X_Range < 2.0 and X_Range >= 0.002:
            Xrange = np.arange((-X_Range*1000)/2.0,(X_Range*1000)/2.0,X_Range*1000.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion * 1000.0
        elif X_Range < 0.002 and X_Range >= 0.000002:
            Xrange = np.arange((-X_Range*1000000)/2.0,(X_Range*1000000)/2.0,X_Range*1000000.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion * 1000000.0
        else:
            Xrange = np.arange((-X_Range*1000000000)/2.0,(X_Range*1000000000)/2.0,X_Range*1000000000.0/Sample_point)
            Timebase_Poistion_X = Timebase_Poistion * 1000000000.0
        #print Xrange
        #time.sleep(10)

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
        print len(totalContent)
        length = len(totalContent[3:])              #print length
        print length/2
        for i in xrange(length/2):              #store data into file
            digital_number = (ord(totalContent[3+i*2+1])<<8)+ord(totalContent[3+i*2])
            if (ord(totalContent[3+i*2+1]) & 0x80) == 0x80:             
                #outfile.write("%f %f\n"%(Xrange[i] + Timebase_Poistion_X, (digital_number - 65535+1000)*Y_Factor + CH1_Offset))
                pass
            else:
                pass
                #outfile.write("%f %f\n"%(Xrange[i] + Timebase_Poistion_X, (digital_number+1000)*Y_Factor + CH1_Offset))

#========================================================#
## if statement
#
if __name__ == '__main__':
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
    ss.connect((hostname,port))                                 #connect to the server
    main()
    ss.close()                                                  #close socket

