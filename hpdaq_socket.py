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
    # @param ss socket name
    def __init__(self, ss):
        self.ss = ss

    ## write config_reg
    # @param Addr Address of the configuration register 0-31 
    # @param Data write into the configuration register 0-65535, [15:0]
    def write_config_reg(self, Addr, Data):
        data = 0x00200000 + (Addr << 16) + Data
        self.ss.sendall(struct.pack('I',data)[::-1])
    
    ## read config_reg
    # @param Addr Address of the configuration register 0-31 
    # return 32bit data
    def read_config_reg(self, Addr):
        data = 0x80200000 + (Addr << 16) 
        self.ss.sendall(struct.pack('I', data)[::-1])
        return struct.unpack('I', self.ss.recv(4)[::-1])[0]

    ## write pulse_reg
    # @param Data write into the pulse register 0-65535
    def write_pulse_reg(self, Data):
        data = 0x000b0000 + Data
        self.ss.sendall(struct.pack('I',data)[::-1])

    ## read status_reg
    # @param Addr Address of the configuration register 0-10
    def read_status_reg(self, Addr):
        data = 0x80000000 + (Addr << 16)
        self.ss.sendall(struct.pack('I',data)[::-1])
        return struct.unpack('I', self.ss.recv(4)[::-1])[0]

    ## write memeoy
    # @param Addr write address of memeoy 0-65535
    # @param Data write into memory data 0-65535
    def write_memory(self, Addr, Data):
        data = 0x00110000 + (0x0000ffff & Addr)             #memory address LSB register
        self.ss.sendall(struct.pack('I',data)[::-1])
        data = 0x00120000 + ((0xffff0000 & Addr) >> 16)     #memory address MSB register
        self.ss.sendall(struct.pack('I',data)[::-1])
        data = 0x00130000 + (0x0000ffff & Data)             #memory Data LSB register
        self.ss.sendall(struct.pack('I',data)[::-1])
        data = 0x00140000 + ((0xffff0000 & Data) >> 16)     #memory Data MSB register
        self.ss.sendall(struct.pack('I',data)[::-1])

    ## read memory
    # @param Cnt read data counts 0-65535
    # @param Addr start address of read memory 0-65535
    def read_memory(self, Cnt, Addr): 
        data = 0x00100000 + Cnt                             #write sMemioCnt
        self.ss.sendall(struct.pack('I',data)[::-1])
        data = 0x00110000 + (0x0000ffff & Addr)             #write memory address LSB register
        self.ss.sendall(struct.pack('I',data)[::-1])
        data = 0x00120000 + ((0xffff0000 & Addr) >> 16)     #write memory address MSB register
        self.ss.sendall(struct.pack('I',data)[::-1])
        data = 0x80140000                                   #read Cnt 32bit memory words  
        self.ss.sendall(struct.pack('I',data)[::-1])
        for i in xrange(Cnt):
            print hex(struct.unpack('I', self.ss.recv(4)[::-1])[0])

    ## read_data_fifo
    # @param Cnt read data counts 0-65535
    def read_data_fifo(self, Cnt):
        data = 0x001a0000 + 0x0000ffff                      #write sDataFifoHigh address = 26
        self.ss.sendall(struct.pack('I',data)[::-1])
        data = 0x00190000 + Cnt                             #write sDataFifoHigh address = 25
        self.ss.sendall(struct.pack('I',data)[::-1])
        for i in xrange(Cnt):
            print hex(struct.unpack('I', self.ss.recv(4)[::-1])[0])

#======================================================================#
## main function
#
def main():
    print "OK!"
#======================================================================#
if __name__ == "__main__":
    ## host socket
    # @param AF_UNIX:AF_Local, base on the local
    # @param AF_NETLINK:linux operating system support socket
    # @param AF_INET:base on IPV4 network TCP/UDP socket
    # @param AF_INET6:base on IPV6 network TCP/UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #establish socket
    s.connect((hostname, port))                                 #connet socket
    cmd_interpret = command_interpret(s)
    #for i in xrange(32):                                       
    #    print "Write in data: %d"%i
    #    cmd_interpret.write_config_reg(i,i+100)                 #write config_reg
    #    print "Read back data: %d"%cmd_interpret.read_config_reg(i) #read config_reg
    #    time.sleep(0.1)

    #for i in xrange(100000):                                     #write pulse_reg
    #    cmd_interpret.write_pulse_reg(0xffff)
    #    time.sleep(0.003)

    #for i in xrange(11):                                        #write 11*16bit data to config_reg    
    #    cmd_interpret.write_config_reg(i,0xaaa0+i)
    #    print "write into config_reg: %d"%cmd_interpret.read_config_reg(i)
    #    cmd_interpret.write_pulse_reg(0xffff)
    #    time.sleep(0.001)
    #for i in xrange(11):                                        #read 11*16bit data from status_reg
    #    print "read from status_reg: %d"%cmd_interpret.read_status_reg(i)   

    #for i in xrange(256):
    #    cmd_interpret.write_memory(i,0xaaaaff00+i) 
    #    #time.sleep(0.01) 
    #cmd_interpret.read_memory(20, 0x0000001f)

    for i in xrange(510): 
        cmd_interpret.write_config_reg(0,i)
        cmd_interpret.write_config_reg(1,0xaaaa)
        cmd_interpret.write_pulse_reg(0x8000)
    cmd_interpret.read_data_fifo(20)
    s.close()                                                   #close socket
    sys.exit(main())                                            #execute main function 
