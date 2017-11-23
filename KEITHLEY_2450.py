#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket
import platform
import subprocess
import numpy as np
#hostname = '192.168.1.119'                  #wire network hostname
hostname = '192.168.2.100'                  #wire network hostname
port = 5025                                 #host tcp port number
#-------------------------------------------------------------------#
def main():
    print "Ok!"
    print platform.system()
    print platform.machine()
    print platform.processor()
    print platform.python_build()
    print platform.python_compiler()
    print platform.python_version()
    print platform.version()
    print platform.uname()
#-------------------------------------------------------------------#
if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
    ss.connect((hostname, port))                                #connect to the instrument 
    main()
    #ret = ss.send("*IDN?;")
    ret = ss.send("*IDN?;")                                     #query instrument ID
    print ret
    print "Instrument ID: %s"%ss.recv(50)
    ss.close()                                                  #close socket
