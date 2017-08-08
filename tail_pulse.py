#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Perform digital threshold scan of the Topmetal-II- sensor
    one row at a time
    Control RIGOL function generator
"""
#*****************************************************************************************#
import time                         #import moudle
import os
import sys
import subprocess
import math
import visa                     #windows instrument driver
#*****************************************************************************************#
def writeSleep(instr, string, sleeptime=0.5):       #write instruction and wait
    instr.write(string)
    time.sleep(sleeptime)
#*****************************************************************************************#
def tailPulse(instr, xp=16, np=1024, sigma=0.001):      #generate tail pulse
    amax = 16383
    vals=[0 for i in xrange(np)]
    for i in xrange(np):
        if i<xp:
            vals[i]=amax
        else:
            vals[i]=int(amax*(1-math.exp(-(i-xp)*sigma)))
        #print(vals[i])
    string = "DATA:DAC VOLATILE"
    for i in xrange(np):
        string +=(",%d"% vals[i])
    writeSleep(instr, string, 1.0)
    writeSleep(instr, "FUNC:USER VOLATILE")

#*****************************************************************************************#
def fungen():
    rm = visa.ResourceManager()         #start visa32.dll
    print rm.list_resources()                 #list the connected instrument
    instr = rm.open_resource('USB0::0x1AB1::0x0641::DG4C143100554::INSTR')
    print instr.query("*IDN?")
    #square_pulse(instr,1024*2, freq, time)
    tailPulse(instr, xp=512, np=1024, sigma=0.01)
    writeSleep(instr, "FREQ %d" %100)
    writeSleep(instr, "VOLT:UNIT VPP") 
    writeSleep(instr, "VOLTage:LOW 0")
    writeSleep(instr, "VOLT:HIGH %f" % 0.05)
    writeSleep(instr, "OUTP ON")
    instr.close()
#*****************************************************************************************#
def main():                             #main function
    fungen()
    print "OK"
#*****************************************************************************************#
if __name__ == "__main__":              #execute main function
    sys.exit(main())
