#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
import datetime
import threading
import numpy as np
'''
@author: WeiZhang
@date: 2018-01-12
Query current value from KEITHLEY source meter and fetch waveform data form Keysight via LXI protocol
'''
SMU_hostname = '192.168.2.100'                  #KELITHLEY source meter ip address
SMU_port = 5025                                 #host tcp port number

Key_hostname = '192.168.2.4'                    #keysight oscilloscope ip address
Key_port = 5025                                 #host tcp port number
 
#-------------------------------------------------------------------#
## save current time and ouput current
def save_time_curr():
    with open("./time_current.dat", 'a') as infile:
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) #acquire cuurent date and time
        print ts
        s1.send(":READ?\n")                                     #read current of the output
        Output_current = float(s1.recv(100))                    #receive output current value
        infile.write("%s %f\n"%(ts, Output_current))
    return ts
#-------------------------------------------------------------------#
def run_task(): 
    print "task is running!"
#-------------------------------------------------------------------#
## fetch data from oscilloscope
def fetch_data(filename):
    with open(filename, 'w') as outfile:
        s2.send(":TIMebase:POSition?;")             #Query X-axis timebase position 
        Timebase_Poistion = float(s2.recv(128)[1:])
        print "Timebase_Position:%.6f"%Timebase_Poistion

        s2.send(":WAVeform:XRANge?;")               #Query X-axis range 
        X_Range = float(s2.recv(128)[1:])
        print "XRange:%f"%X_Range

        s2.send(":WAVeform:YRANge?;")               #Query Y-axis range
        Y_Range = float(s2.recv(128)[1:])
        print "YRange:%f"%Y_Range
        Y_Factor = Y_Range/62712.0

        s2.send(":ACQuire:POINts:ANALog?;")         #Query analog store depth
        Sample_point = int(s2.recv(128)[1:]) - 3
        print "Sample Point:%d"%Sample_point

        s2.send(":WAVeform:XUNits?;")               #Query X-axis unit 
        print "X-axis Unit:%s"%(s2.recv(128)[1:])

        s2.send(":WAVeform:YUNits?;")               #Query Y-axis unit 
        print "Y-axis Unit:%s"%(s2.recv(128)[1:])

        s2.send(":CHANnel1:OFFset?;")               #Channel1 Offset 
        CH1_Offset = float(s2.recv(128)[1:])
        print "Channel 1 Offset:%f"%CH1_Offset

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

        s2.send(":ACQuire:SRATe:ANALog?;")          #Query sample rate
        Sample_Rate = float(s2.recv(128)[1:])
        print "Sample rate:%.1f"%Sample_Rate
        total_point = Sample_Rate * X_Range
        print total_point

        s2.send(":SYSTem:HEADer OFF;")              #Query analog store depth
        s2.send(":WAVeform:SOURce CHANnel1;")       #Waveform source 
        s2.send(":WAVeform:BYTeorder LSBFirst;")    #Waveform data byte order
        s2.send(":WAVeform:FORMat WORD;")           #Waveform data format
        s2.send(":WAVeform:STReaming 1;")           #Waveform streaming on
        s2.send(":WAVeform:DATA? 1,%d;"%int(total_point))         #Query waveform data with start address and length
        n = total_point * 2 + 3
        print "n = %d"%n                            #calculate fetching data byte number
        totalContent = ""
        totalRecved = 0
        while totalRecved < n:                      #fetch data
            #print n, (n-totalRecved)
            onceContent = s2.recv(int(n - totalRecved))
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
        print "fetch data over!!!"
#-------------------------------------------------------------------#
def timeFun(sched_Timer, time_slot):
    flag = 0
    while True:
        now = datetime.datetime.now()               #acquire current time
        #print now, sched_Timer
        if now.hour==sched_Timer.hour and now.minute==sched_Timer.minute and now.second==sched_Timer.second and flag==0:
            run_task()                              #run task one
            time_str = save_time_curr()             #save time and current
            filename = "./fetch_data/" + time_str + ".dat"
            fetch_data(filename)
            flag = 1                                #set flag
        else:
            if flag==1:
                sched_Timer = sched_Timer + datetime.timedelta(seconds=time_slot)   #set time slot
                flag = 0;                           #reset flag
#-------------------------------------------------------------------#
## main function: used to test the resistor of the load
def main():
    with open("./time_current.dat", 'w') as infile:
        infile.truncate()
        s1.send("*IDN?\n")                                      #command terminated with '\n'
        print "Keithley instrument ID: %s"%s1.recv(50)
        s1.send("*RST\n")                                       #command terminated with '\n'
        s1.send("SENS:CURR:RANG 1000E-3\n")                     #set the current range 10mA
        s1.send("DISP:DIG 6\n")                                 #display digital the max is 6
        s1.send("OUTP ON\n")                                    #open output

        s2.send("*IDN?\n")                                      #command terminated with '\n'
        print "Keysight instrument ID: %s"%s2.recv(100)

        sched_Timer = datetime.datetime.now() + datetime.timedelta(seconds=5)
        time_slot = float(sys.argv[1])
        timeFun(sched_Timer, time_slot)
        print "OK!"
#-------------------------------------------------------------------#
## if statement
if __name__ == "__main__":
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
    s1.connect((SMU_hostname, SMU_port))                        #connect to the instrument 

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
    s2.connect((Key_hostname, Key_port))                        #connect to the instrument

    main()
    s1.close()                                                  #close socket
    s2.close()                                                  #close socket
 
