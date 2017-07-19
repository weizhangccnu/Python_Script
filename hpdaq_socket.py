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
        data = 0x00190000 + Cnt                             #write sDataFifoHigh address = 25
        self.ss.sendall(struct.pack('I',data)[::-1])
        for i in xrange(Cnt):
            print hex(struct.unpack('I', self.ss.recv(4)[::-1])[0])

#======================================================================#
def test_config_reg():
    for i in xrange(32):                                       
        print "Write in data: %d"%i
        cmd_interpret.write_config_reg(i,i+100)                     #write config_reg
        print "Read back data: %d"%cmd_interpret.read_config_reg(i) #read config_reg
        time.sleep(0.1)

#======================================================================#
def test_pulse_reg():
    for i in xrange(100000):                                     #write pulse_reg
        cmd_interpret.write_pulse_reg(0xffff)
        time.sleep(0.03)

#======================================================================#
def test_status_reg():
    for i in xrange(11):                                        #write 11*16bit data to config_reg 
        cmd_interpret.write_pulse_reg(0x0001)
        cmd_interpret.write_config_reg(i,0xaaa0+i)
        print "write into config_reg: %d"%cmd_interpret.read_config_reg(i)
        time.sleep(0.001)
    for i in xrange(11):                                        #read 11*16bit data from status_reg
        print "read from status_reg: %d"%cmd_interpret.read_status_reg(i)
#======================================================================#
def test_memory():
    for i in xrange(256):
        cmd_interpret.write_memory(i,0xaaaaff00+i) 
        time.sleep(0.01) 
    cmd_interpret.read_memory(20, 0x00000000)

#======================================================================#
def test_data_fifo():
    cmd_interpret.write_config_reg(2,0x0000)                    #write disable
    for i in xrange(5):                                         #generate 5 clcok period after reset
        cmd_interpret.write_pulse_reg(0x8000)                   
    #time.sleep(0.1)
    cmd_interpret.write_config_reg(2,0x0001)                    #write enable
    for i in xrange(10):                                        #write 10 data to fifo
        cmd_interpret.write_config_reg(0,i)
        cmd_interpret.write_config_reg(1,0xaaaa)
        time.sleep(0.01)
        cmd_interpret.write_pulse_reg(0x8000)                   #generate clock to write data
        for i in xrange(2):
            print "Read back data: %d"%cmd_interpret.read_config_reg(i) #read config_reg
    cmd_interpret.read_data_fifo(5)                             #read data from fifo

#======================================================================#
## write 32bit data to dac8568
# @param dat write into dac8568's data
def dac8568_write_data(dat):
    cmd_interpret.write_config_reg(0,(0xffff0000&dat)>>16)  #write high word to fifo
    cmd_interpret.write_pulse_reg(0x0002)                   #generate write pulse  
    cmd_interpret.write_config_reg(0,0xffff&dat)            #write low word to fifo
    cmd_interpret.write_pulse_reg(0x0002)                   #generate write pulse
#======================================================================#
## test dac8568 via hpdaq FPGA development board
# @param ch choose the dac8568 channel 0-15
# @param data dac8568 write in digital data 0-5V
def test_dac8568(ch, val):
    data = int((val*65535.0)/5.0)
    if ch >= 0 and ch <=7:
        cmd_interpret.write_config_reg(1,0x0001)                #select dac8568 one
    elif ch >7 and ch <= 15:
        cmd_interpret.write_config_reg(1,0x0000)                #select dac8568 two 
    else:
        print "you input error channel unmber"
    dat = 0x58000001                                        #enable internal reference 
    dac8568_write_data(dat)
    dat = 0x5000000a + (ch << 20)+ (data << 4)              #write to selected channel input register 
    dac8568_write_data(dat)
    dat = 0x5100000a + (ch << 20) + (data << 4)             #update selected channel register 
    dac8568_write_data(dat)
    
#======================================================================#
## main function
#
def main():
    #test_config_reg()  
    #test_pulse_reg()  
    #test_status_reg()
    #test_memory()
    #test_data_fifo()
    for i in xrange(10):
        print i
        for ch in xrange(16):
            test_dac8568(ch, i*0.33)
            time.sleep(0.1) 
        time.sleep(5) 
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
    sys.exit(main())                                     		#execute main function 
    s.close()                                                   #close socket
				
