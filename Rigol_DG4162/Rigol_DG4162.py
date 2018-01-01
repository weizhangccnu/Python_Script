#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
import platform
'''
@author: Wei Zhang
This python script is used to connect PC and Rigol DG4162 via Ethernet cable on Linux operating system
'''
hostname = '192.168.2.3'    #IP address
port = 5555                 #Rigol Ethernet port number
#************************************************************************#
def main():
    ss.send("*IDN?\n")                          #query instrument ID
    print ss.recv(50)
    for i in xrange(100):
        step = i * 100
        print "CH1 Output Frequency: %dHz"%step
        ss.send(":SOURce1:FREQuency %s\n"%step)
        time.sleep(0.5)
    print "OK!"
#************************************************************************#
if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
    ss.connect((hostname, port))
    main()
