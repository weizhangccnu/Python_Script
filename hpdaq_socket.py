#!/usr/bin/env python
# -*- coding:utf-8 -*-

## @package HPDAQ socket communication
# control hpdaq via socket
import os
import sys
import time
import socket
import struct

hostname = "192.168.2.3"            #server ip address
port = 1024                         #server port number
#======================================================================#
## Command interpret
class command_interpret:
    ## constructor
    # @para ss socket name
    def __init__(self, ss):
        self.ss = ss

    ## write config_reg
    # @para Addr Address of the configuration register 0-31 [27:16]
    # @para Data wri0te to configuration register data 0-65535, [15:0]
    def write_config_reg(self, Addr, Data):
        data = 0x00200000 + (Addr << 16) + Data
        stri = struct.pack('I',data)
        self.ss.sendall(stri[::-1])
    
    ## read config_reg
    # @para Addr Address of the configuration register 0-31 [27:16]
    # return 32bit data
    def read_config_reg(self, Addr):
        data = 0x80200000 + (Addr << 16) 
        stri = struct.pack('I', data)
        self.ss.sendall(stri[::-1])
        return struct.unpack('I', self.ss.recv(4)[::-1])[0]
#======================================================================#
## main function
#
def main():
    print "OK!"
#======================================================================#
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #establish socket
    s.connect((hostname, port))                                 #connet socket
    cmd_interpret = command_interpret(s)
    for i in xrange(32):                                       
        print "Write in data: %d"%i
        cmd_interpret.write_config_reg(i,i+100)                 #write config_reg
        print "Read back data: %d"%cmd_interpret.read_config_reg(i) #read config_reg
        time.sleep(0.1)
    s.close()                                                   #close socket
    sys.exit(main())     
