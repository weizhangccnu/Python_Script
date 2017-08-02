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
if __name__ == '__main__':
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #init local socket handle
    ss.connect((hostname,port))                                 #connect to the server
    print ss.send("*IDN?;")                                     #send data to server from the local socket handle:ss
    data = ss.recv(512)
    print data
    print "OK!"
    for i in xrange(201):
        ss.send(':CHANnel1:OFFSet %s;'%str(i*0.01))                   #send data to server from the local socket handle:ss
        time.sleep(0.1)
    #print data
    ss.close()
