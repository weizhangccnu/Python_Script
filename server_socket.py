#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
import socket 
#AF_INET,SOCK_STREAM
#import socket
hostname = "10.149.88.74"	    #host name
port = 8011			            #host tcp port
#==========================================================
## main function
def main():
	print "OK!"
#==========================================================#
if __name__ == "__main__":
	#init local socket handle
	##family host
	# @param AF_UNIX:AF_Local, base on the local
	# @param AF_NETLINK:linux operating system support socket
	# @param AF_INET:base on IPV4 network TCP/UDP socket
	# @param AF_INET6:base on IPV6 network TCP/UDP socket
	
	##socket type
	# @param SOCKET_STREAM:stream socket for TCP
	# @param SOCKET_DGRAM:graph socket for UDP
	# @param SOCKET_RAM:raw socket
	ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	ss.bind((hostname, port))
	ss.listen(10)		        	#listen to the port
	i = 0
	while 1:
		i += 1
		conn, addr = ss.accept()	#new a socket
		print "got connected from",addr	#pirnt IP address
		conn.send("%d byebye"%i)	#send a string
		data = conn.recv(512)		#receive data
		print data
		time.sleep(0.1)
	conn.close()
	ss.close()
	sys.exit(main())
