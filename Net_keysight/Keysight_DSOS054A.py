#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
import subprocess
import numpy as np
#hostname = "192.168.2.3"                #wire network hostname
hostname = "10.146.77.37"              #wireless network hostname
port = 5025                             #host tcp port
#note that: every command should be termianated with a semicolon
#========================================================#
## plot waveform via gnuplot with parameters
# @param x_range x-axis range scope
# @param y_range y2-axis range scope
# @param ch1_offset channel one offset 
# @param timebase_position x-axis timebase position 
def plot(x_range,y_range,ch1_offset,timebase_position,x_unit):
   XRange = "x_var='%.5f'"%(x_range)            #xrange parameter 
   YRange = "y_var='%.3f'"%(y_range)            #yrange parameter
   CH1offset = "offset='%.3f'"%(ch1_offset)     #offset parameter
   Timebase_Position = "timebase_position='%.5f'"%(timebase_position)     #timebase position parameter
   X_Unit = "x_unit='%d'"%(x_unit)              #x-axis unit parameter
   print XRange,YRange,CH1offset,Timebase_Position,X_Unit
   subprocess.call("gnuplot -e %s -e %s -e %s -e %s -e %s keysight_oscilloscope.gp"%(XRange,YRange,CH1offset,Timebase_Position,X_Unit), shell = True)
   subprocess.call("eps2png -resolution 400 keysight_oscilloscope.eps", shell = True)
   subprocess.call("xdg-open keysight_oscilloscope.png", shell = True)
   print "OK"
#========================================================#
## main function: sent oscilloscope commands and fetch data
#
def main():
    with open("./data_output.dat",'w') as outfile:
        Timebase_scale = 0
        ss.send("*IDN?;")                           #read back device ID
        print "Instrument ID: %s"%ss.recv(128)   

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
                outfile.write("%f %f\n"%(Xrange[i] + Timebase_Poistion_X, (digital_number - 65535+1000)*Y_Factor + CH1_Offset))
            else:
                outfile.write("%f %f\n"%(Xrange[i] + Timebase_Poistion_X, (digital_number+1000)*Y_Factor + CH1_Offset))
    return [X_Range,Y_Range,CH1_Offset,Timebase_Poistion]             #return gnuplot parameters
#========================================================#
## if statement
#
if __name__ == '__main__':
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
    ss.connect((hostname,port))                                 #connect to the server
    xyrange = []
    xyrange = main()
    print xyrange 
    if xyrange[0] >= 2.0:                                       #x-axis unit is second
        x_range = xyrange[0]*0.5    
        timebase_poistion = xyrange[3]
        x_unit = 1
    elif xyrange[0] < 2.0 and  xyrange[0] >= 0.002:             #x-axis unit is millisecond
        x_range = xyrange[0]*500
        timebase_poistion = xyrange[3] * 1000.0
        x_unit = 2
    elif xyrange[0] < 0.002 and  xyrange[0] >= 0.000002:        #x-axis unit is microsecond
        x_range = xyrange[0]*500000
        timebase_poistion = xyrange[3] * 1000000.0
        x_unit = 3
    else:                                                       #x-axis unit is nanosecond
        x_range = xyrange[0]*500000000
        timebase_poistion = xyrange[3] * 1000000000.0
        x_unit = 4
    plot(x_range,xyrange[1]*0.5,xyrange[2],timebase_poistion,x_unit)   #plot waveform using fetched data
    ss.close()
