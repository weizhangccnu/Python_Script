#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
hostname = "192.168.2.3"                #hostname
port = 5025                             #host tcp port
#note that: every command should be termianated with a semicolon
#========================================================#
## main function
#
def main():
    with open("./data_output.dat",'w') as outfile:
        Timebase_scale = 0
        ss.send("*IDN?;")                           #read back device ID
        print ss.recv(128)   
        ss.send(":TIMebase:SCALe?;")                #Time base scale
        Timebase_scale = float(ss.recv(128)[1:])   
        print Timebase_scale

        ss.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
        print int(ss.recv(128)[1:])   

        ss.send(":ACQuire:SRATe:ANALog?;")          #Query sample rate
        Sample_Rate = float(ss.recv(128)[1:])   
        print Sample_Rate
        total_point = Sample_Rate * 10 * Timebase_scale
         
        ss.send(":SYSTem:HEADer OFF;")              #Query analog store depth
        ss.send(":WAVeform:SOURce CHANnel1;")       #Query analog store depth
        ss.send(":WAVeform:BYTeorder LSBFirst;")    #Query analog store depth
        ss.send(":WAVeform:FORMat WORD;")           #Query analog store depth
        ss.send(":WAVeform:STReaming 1;")           #Query analog store depth
        #ss.send(":WAVeform:DATA? 1,%d;"%(Sample_Rate * 10 * Timebase_scale))                 #Query analog store depth
        ss.send(":WAVeform:DATA? 1,%d;"%int(total_point))         #Query analog store depth
        string = ""
        for i in xrange((int(total_point)/1446)+1): 
            string += ss.recv(1280000000)
        print string
        length = len(string[3:])
        print length
        #for i in xrange(length/2):
        #    print i,(ord(string[3+i*2+1])<<8) + ord(string[3+i*2])
        #    outfile.write("%d %d\n"%(i, (ord(string[3+i*2+1])<<8) + ord(string[3+i*2])))
#========================================================#
## if statement
#
if __name__ == '__main__':
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
    ss.connect((hostname,port))                                 #connect to the server
    main()
    ss.close()
