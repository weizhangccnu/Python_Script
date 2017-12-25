#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
import platform
import subprocess
import numpy as np
hostname = '192.168.2.100'                  #wire network hostname
port = 5025                                 #host tcp port number
#-------------------------------------------------------------------#
def main():
    ss.send("*IDN?\n")                                          #command terminated with '\n'
    print "Instrument ID: %s"%ss.recv(50)
    ss.send("*RST\n")                                           #command terminated with '\n'
    ss.send(":SOUR:FUNC VOLT\n")
    ss.send(':SENS:FUNC "CURR"\n')
    ss.send("SENS:CURR:RANG 1\n")
    ss.send("DISP:DIG 5\n")
    ss.send("OUTP ON\n")
    for i in xrange(30):
        ss.send(":SOUR:VOLT %d\n"%i)
        time.sleep(1)
        ss.send(":READ?\n")
        print ss.recv(100)
    ss.close()                                                  #close socket
    print "Ok!"
#-------------------------------------------------------------------#
if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
    ss.connect((hostname, port))                                #connect to the instrument 
    main()

