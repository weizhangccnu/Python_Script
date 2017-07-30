#!/usr/bin/env python
# -*- coding:utf8 -*-
import os 
import sys
import time
import socket 
hostname = "10.144.1.9"				#hostname
port = 8011								#host tcp port

#========================================================#
if __name__ == '__main__':
	
	while 1:
		for i in xrange(10):
			ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)		#init local socket handle
			ss.connect((hostname,port))			#connect to the server
			ss.send(str(i))		#send data to server from the local socket handle:ss
			time.sleep(0.1)
			data = ss.recv(512)
			print data
	ss.close()							#close the socket connection
