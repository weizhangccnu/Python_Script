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
    # @param[in] ss socket name
    def __init__(self, ss):
        self.ss = ss

    ## write config_reg
    # @param[in] Addr Address of the configuration register 0-31 
    # @param[in] Data write into the configuration register 0-65535, [15:0]
    def write_config_reg(self, Addr, Data):
        data = 0x00200000 + (Addr << 16) + Data
        self.ss.sendall(struct.pack('I',data)[::-1])
    
    ## read config_reg
    # @param[in] Addr Address of the configuration register 0-31 
    # return 32bit data
    def read_config_reg(self, Addr):
        data = 0x80200000 + (Addr << 16) 
        self.ss.sendall(struct.pack('I', data)[::-1])
        return struct.unpack('I', self.ss.recv(4)[::-1])[0]

    ## write pulse_reg
    # @param[in] Data write into the pulse register 0-65535
    def write_pulse_reg(self, Data):
        data = 0x000b0000 + Data
        self.ss.sendall(struct.pack('I',data)[::-1])

    ## read status_reg
    # @param[in] Addr Address of the configuration register 0-10
    def read_status_reg(self, Addr):
        data = 0x80000000 + (Addr << 16)
        self.ss.sendall(struct.pack('I',data)[::-1])
        return struct.unpack('I', self.ss.recv(4)[::-1])[0]

    ## write memeoy
    # @param[in] Addr write address of memeoy 0-65535
    # @param[in] Data write into memory data 0-65535
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
    # @param[in] Cnt read data counts 0-65535
    # @param[in] Addr start address of read memory 0-65535
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
    # @param[in] Cnt read data counts 0-65535
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
# @param[in] dat write into dac8568's data
def dac8568_write_data(dat):
    cmd_interpret.write_config_reg(0,(0xffff0000&dat)>>16)  #write high word to fifo
    cmd_interpret.write_pulse_reg(0x0002)                   #generate write pulse  
    cmd_interpret.write_config_reg(0,0xffff&dat)            #write low word to fifo
    cmd_interpret.write_pulse_reg(0x0002)                   #generate write pulse

#======================================================================#
## test dac8568 via hpdaq FPGA development board
# @param[in] ch choose the dac8568 channel 0-15
# @param[in] data dac8568 write in digital data 0-5V
def test_dac8568(ch, val):
    data = int((val*65535.0)/5.0)                           #convert voltage value to digital code
    if ch >= 0 and ch <= 7:
        cmd_interpret.write_config_reg(1,0x0001)            #select dac8568 one
    elif ch >= 8 and ch <= 15:
        ch = ch - 8
        cmd_interpret.write_config_reg(1,0x0000)            #select dac8568 two 
    else:
        print "you input error channel unmber"
    dat = 0x58000001                                        #enable internal reference 
    dac8568_write_data(dat)
    dat = 0x5000000a + (ch << 20)+ (data << 4)              #write to selected channel input register 
    dac8568_write_data(dat)
    dat = 0x5100000a + (ch << 20) + (data << 4)             #update selected channel register 
    dac8568_write_data(dat)
    
#======================================================================#
## shift register write and read function
# @param[in] data 170bit value to be sent to the TMIIa shift register
# @param[in] clk_div clock frequency division factor:(clk/2**clk_div) [5:0]
def shift_register_wr(data, clk_div):
    div_reg = (clk_div & 0x3f) << 170                       #config_reg[175:170]
    data_reg = data & ((1 << 170)-1)                        #config_reg[169:0]
    val = div_reg | data_reg
    print bin(val)
    for i in xrange(11):                                    #write 176bit to config register
        cmd_interpret.write_config_reg(i,(val >> i*16) & 0xffff)
    cmd_interpret.write_pulse_reg(0x0001)                   #pulse_reg[0] generate a pulse
    for i in xrange(11): 
        print bin(cmd_interpret.read_status_reg(i))

#======================================================================#
## This function is used to config  topmetal-IIa sram and array scan modules
# @param[in] start_addr address of first data sent to sram
# @param[in] data_to_sram data sent to sram
def tm_sram_config(start_addr, data_to_sram): 
    nval = int((len(data_to_sram)+7)/8)
    addr = start_addr & ((1<<32)-1)
    aval = [0 for i  in xrange(nval)]
    for i in xrange(len(data_to_sram)):
        j = i % 8
        k = i / 8
        aval[k] += data_to_sram[j] << (j*4)
    for i in xrange(len(aval)):
        cmd_interpret.write_memory(addr+i, aval[i])
    cmd_interpret.write_memory(len(aval), addr)

#======================================================================#
## topmetal array scan config function
# @param[in] clk_div clock frequency division factor when array is scanning
# @param[in] wr_clk_div clock frequency division factor when writing data into pixel
# @param[in] stop_addr controls where scanning stop
def tm_array_scan(clk_div, wr_clk_div, stop_addr, trig_rate, trig_delay, stop_clk_s, keep_we):
    config_reg = ((trig_delay & 0xffff) << 48) | ((trig_rate & 0xffff) << 32) | ((stop_addr & 0xffff) <<16) | ((keep_we & 0x1) << 9) | ((stop_clk_s & 0x1) << 8) | ((wr_clk_div & 0xf) << 4) | (clk_div & 0xf)
    for i in xrange(4):
        cmd_interpret.write_config_reg(i+11, (config_reg >> i*16) & 0xffff) 
    cmd_interpret.write_pulse_reg(0x0004)                   #pulse_reg[2] generate a pulse
#======================================================================#
## main function
#
def main():
    ## config dac8568 
    VBTAIL_RCF_IN = 0.74                                #dac8568 channel 0 ----> VBTAIL_RCF_IN default value 0.74V
    VREF_RCF_IN = 0.1                                   #dac8568 channel 1 ----> VREF_RCF_IN default value 0.1V
    VBP_RCF_IN = 2.2                                    #dac8568 channel 2 ----> VBP_RCF_IN default value 2.2V
    SF1_IBP_RCF_IN = 1.6                                #dac8568 channel 3 ----> SF1_IBP_RCF_IN default value 1.6V
    CSA_VBN = 0.77                                      #dac8568 channel 4 ----> CSA_VBN default value 0.77V
    CSA_VRSTL_VG = 3.3                                  #dac8568 channel 5 ----> CSA_VRSTL_VG default value 3.3V
    CSA_VRSTL = 0.23                                    #dac8568 channel 6 ----> CSA_VRSTL default value 0.23V
    CSA_VRSTH = 0.3                                     #dac8568 channel 7 ----> CSA_VRSTH default value 0.3V
    COL_IB_ICF_IN = 0.4                                 #dac8568 channel 12 ----> COL_IB_ICF_IN default value 0.4V, the rest of channel's output value are 0V
    dac_val = [VBTAIL_RCF_IN, VREF_RCF_IN, VBP_RCF_IN, SF1_IBP_RCF_IN, CSA_VBN, CSA_VRSTL_VG, CSA_VRSTL, CSA_VRSTH, 0, 0, 0, 0, COL_IB_ICF_IN, 0, 0, 0]
    for i in xrange(len(dac_val)):
        print i, dac_val[i]
        test_dac8568(i, dac_val[i])                          
        time.sleep(0.1)
    ## config shift register 
    dac1 = 0xffff
    dac2 = 0xffff
    dac3 = 0xffff
    dac4 = 0xffff
    dac5 = 0xffff
    dac6 = 0xffff
    dac7 = 0xffff
    dac8 = 0xffff
    dac9 = 0xffff
    VBTail_RCF = 0b0010
    VREF_RCF = 0b0010
    VBP_RCF = 0b0010
    SF_IBP = 0b0010
    D_BUFFER_EN = 0b1
    A_BUFFER_EN = 0b1
    CMOSSW_Bias = 0b1
    COL_IB_RCF = 0b0010
    NC = 0b000

    data_in = (dac9<<151)+(COL_IB_RCF<<147)+(CMOSSW_Bias<<146)+(A_BUFFER_EN<<145)+(D_BUFFER_EN<<144)+(dac1<<128)+(dac3<<112)+(dac2<<96)+(dac8<<80)+(SF_IBP<<76)+(dac5<<60)+(VBP_RCF<<56)+(dac4<<40)+(VREF_RCF<<36)+(dac6<<20)+(VBTail_RCF<<16)+(dac7<<0) 
    print bin(data_in)
    time.sleep(1)
    clk_div = 7    
    shift_register_wr(data_in, clk_div)
    ## config analog scan module
    start_addr = 0
    data_to_sram = [0x8 for i in xrange(9720)]
    tm_sram_config(start_addr, data_to_sram)            #config sram
    time.sleep(3)
    
    clk_div = 6                                         #array scan clock
    wr_clk_div = 5                                      #sram write and read clock
    stop_addr = 1                                       #0x8013  pixel(0,19)
    trig_rate = 4
    trig_delay = 1
    stop_clk_s = 0                                      #0: keep clk running 1: clk stop
    keep_we = 1
    tm_array_scan(clk_div, wr_clk_div, stop_addr, trig_rate, trig_delay, stop_clk_s, keep_we)
    print "OK!"
#======================================================================#
if __name__ == "__main__":
    ## host socket
    # @param[in] AF_UNIX:AF_Local, base on the local
    # @param[in] AF_NETLINK:linux operating system support socket
    # @param[in] AF_INET:base on IPV4 network TCP/UDP socket
    # @param[in] AF_INET6:base on IPV6 network TCP/UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #establish socket
    s.connect((hostname, port))                                 #connet socket
    cmd_interpret = command_interpret(s)                        #define a class
    main()                                                      #execute main function
    s.close()                                                   #close socket
				
