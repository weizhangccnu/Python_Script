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
#-------------------------------------------------------------------#
if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #init local socket handle
    ss.connect((hostname, port))                                #connect to the instrument 
    main()
    ss.send("*IDN?\n")
    print "Instrument ID: %s"%ss.recv(50)
    ss.close()                                                  #close socket
