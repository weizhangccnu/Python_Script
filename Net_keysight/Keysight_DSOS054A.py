#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
import subprocess
hostname = "192.168.2.3"                #hostname
port = 5025                             #host tcp port
#note that: every command should be termianated with a semicolon
#========================================================#
## plto function using gnuplot
#
def plot():
   subprocess.call("gnuplot keysight_oscilloscope.gp", shell = True)
   subprocess.call("eps2png -resolution 300 keysight_oscilloscope.eps", shell = True)
   subprocess.call("xdg-open keysight_oscilloscope.png", shell = True)
   print "OK"
#========================================================#
## main function
#
def main():
    with open("./data_output.dat",'w') as outfile:
        Timebase_scale = 0
        ss.send("*IDN?;")                           #read back device ID
        print ss.recv(128)   

        ss.send(":WAVeform:XRANge?;")               #Query X-axis range 
        Timebase_scale = float(ss.recv(128)[1:])
        print Timebase_scale

        ss.send(":WAVeform:YRANge?;")               #Query Y-axis range
        print float(ss.recv(128)[1:])   
        #time.sleep(10)

        ss.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
        print int(ss.recv(128)[1:])   

        ss.send(":ACQuire:SRATe:ANALog?;")          #Query sample rate
        Sample_Rate = float(ss.recv(128)[1:])   
        print Sample_Rate
        total_point = Sample_Rate * Timebase_scale
         
        ss.send(":SYSTem:HEADer OFF;")              #Query analog store depth
        ss.send(":WAVeform:SOURce CHANnel1;")       #
        ss.send(":WAVeform:BYTeorder LSBFirst;")    #Query analog store depth
        ss.send(":WAVeform:FORMat WORD;")           #Query analog store depth
        ss.send(":WAVeform:STReaming 1;")           #Query analog store depth
        #ss.send(":WAVeform:DATA? 1,%d;"%(Sample_Rate * 10 * Timebase_scale))                 #Query analog store depth
        print total_point
        ss.send(":WAVeform:DATA? 1,%d;"%int(total_point))         #Query analog store depth
        n = total_point * 2 + 3
        print "n = %d"%n
        totalContent = ""
        totalRecved = 0
        while totalRecved < n:
            print n, n-totalRecved
            onceContent = ss.recv(int(n - totalRecved))
            print len(onceContent)
            totalContent += onceContent
            totalRecved = len(totalContent)
        print len(totalContent)
        length = len(totalContent[3:]) #print length
        print length/2
        for i in xrange(length/2):
            if (ord(totalContent[3+i*2+1])<<8) + ord(totalContent[3+i*2]) > 32768:
                outfile.write("%d %d\n"%(i, (ord(totalContent[3+i*2+1])<<8)+ord(totalContent[3+i*2]) - 65535))
            else:
                outfile.write("%d %d\n"%(i, (ord(totalContent[3+i*2+1])<<8)+ord(totalContent[3+i*2])))
#========================================================#
## if statement
#
if __name__ == '__main__':
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
    ss.connect((hostname,port))                                 #connect to the server
    main()
    plot()
    ss.close()
