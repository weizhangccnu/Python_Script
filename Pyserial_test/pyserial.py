#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import struct
import serial
import platform
#=================================================================#
## main function
def main():
    if platform.system() == "Linux":
        print "The operating system is Linux!"
        ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.5)    #open serial port
    else:
        print "The operating system is Windows!"
        ser = serial.Serial('COM1', 9600, timeout=0.5)    #open serial port
    for i in xrange(1000000):               #read 100 charater from stm32
        ser.write('a')                      #sent charater 'a'
        print int(struct.unpack('B',ser.read(1))[0])
        time.sleep(0.05)                    #delay
    print "OK!"                             #stop
#=================================================================#
## if statement
if __name__ == "__main__":
    main()                                  #execute main function
