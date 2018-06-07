#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import copy
import time
import visa
import struct
import socket
from command_interpret import *
'''
@author: Wei Zhang
@date: 2018-03-20
Control module for testing mig ip core and sport120 LLD.
'''
hostname = '192.168.2.3'					#FPGA IP address
port = 1024									#port number
#--------------------------------------------------------------------------#
## DDR3 write data to external device
# @param[in] wr_wrap: wrap address 
# @param[in] wr_begin_addr: write data begin address
# @param[in] post_trigger_addr: post trigger address
def write_data_into_ddr3(wr_wrap, wr_begin_addr, post_trigger_addr):
    # writing begin address and wrap_around
    val = (wr_wrap << 28) + wr_begin_addr
    cmd_interpret.write_config_reg(8, 0xffff & val)
    cmd_interpret.write_config_reg(9, 0xffff & (val >> 16))
    # post trigger address  cmd_interpret.write_config_reg(10, 0xffff & post_trigger_addr)
    cmd_interpret.write_config_reg(11, 0xffff & (post_trigger_addr >> 16))
#--------------------------------------------------------------------------#
## DDR3 read data from fifo to ethernet
# @param[in] rd_stop_addr: read data start address
def read_data_from_ddr3(rd_stop_addr):
    cmd_interpret.write_config_reg(12, 0xffff & rd_stop_addr)
    cmd_interpret.write_config_reg(13, 0xffff & (rd_stop_addr >> 16))
    cmd_interpret.write_pulse_reg(0x0020)           # reading start 
#--------------------------------------------------------------------------#
## test ddr3
def test_ddr3():
    cmd_interpret.write_config_reg(0, 0x0000)       # written disable
    cmd_interpret.write_pulse_reg(0x0040)           # reset ddr3 control logic 
    cmd_interpret.write_pulse_reg(0x0004)           # reset ddr3 data fifo
    print "sent pulse!"

    cmd_interpret.write_config_reg(0, 0x0001)       # written enable

    write_data_into_ddr3(1, 0x0000000, 0x0010000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start 
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop 

    time.sleep(1)
    cmd_interpret.write_config_reg(0, 0x0000)       # write enable
    time.sleep(2)
    read_data_from_ddr3(0x0010000)                  # set read begin address

    ## memoryview usage
    for i in xrange(1):
        cmd_interpret.read_data_fifo(12)            # reading start
#--------------------------------------------------------------------------#
## IIC write slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0] : slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
# @param data[7:0] : 8-bit write data
def iic_write(mode, slave_addr, wr, reg_addr, data):
    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | data
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)           # Sent a pulse to IIC module
    #print hex(val)
#--------------------------------------------------------------------------#
## IIC read slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0]: slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
def iic_read(mode, slave_addr, wr, reg_addr):
	val = mode << 24 | slave_addr << 17 |  0 << 16 | reg_addr << 8 | 0x00	# write device addr and reg addr
	cmd_interpret.write_config_reg(4, 0xffff & val)
	cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
	time.sleep(0.01)
	cmd_interpret.write_pulse_reg(0x0001)				# Sent a pulse to IIC module

	val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | 0x00	# write device addr and read one byte
	cmd_interpret.write_config_reg(4, 0xffff & val)
	cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
	time.sleep(0.01)
	cmd_interpret.write_pulse_reg(0x0001)				# Sent a pulse to IIC module 
	time.sleep(0.01)									# delay 10ns then to read data
	return cmd_interpret.read_status_reg(0) & 0xff
#--------------------------------------------------------------------------#
## capture oscilloscope screen image via GPIB interface 
def capture_screen_image(filename, mode):
	rm = visa.ResourceManager()
	print rm.list_resources()
	inst = rm.open_resource('GPIB0::7::INSTR')
	print inst.query("*IDN?")
	inst.write("*RST")									#set the instrument mode to default setup mode
	time.sleep(1)
	if mode == 1:
		inst.write(":SYSTem:MODE JITTer")					#set the instrument to Jitter mode
		inst.write(":FUNCtion1:SUBTract CHANnel1,CHANnel2")
		inst.write(":FUNCTION1:DISPLAY ON")
		inst.write(":AUToscale")							#Autoscale instrument
		time.sleep(2)
		inst.write(":ACQuire:RUNTil PATTerns,30")			#set patten frame to 30
		inst.write(":ACQuire:SSCReen DISK, '%s'"%filename)	#save screen image to disk
		inst.write(":ACQuire:SSCReen:AREA SCReen")			#capture screen area 
		#inst.write(":ACQuire:SSCReen:IMAGe INVert")			#remove black background
		time.sleep(40)										#delay for acquire limite
	else:
		inst.write(":SYSTem:MODE EYE")						#set the instrument to Eye/Mask Mode
		inst.write(":FUNCtion1:SUBTract CHANnel1,CHANnel2")
		inst.write(":FUNCTION1:DISPLAY ON")
		time.sleep(0.5)
		inst.write(":AUToscale")							#Autoscale instrument
		time.sleep(20)
		inst.write(":MEASure:CGRade:ZLEvel FUNCtion1")		#Measure Zero level 
		inst.write(":MEASure:CGRade:OLEvel FUNCtion1")		#Measure One level
		inst.write(":MEASure:FALLtime FUNCtion1")			#Measure Rise time 
		inst.write(":MEASure:RISetime FUNCtion1")			#Measure Rise time 

		inst.write(":ACQuire:EYELine ON")					#turn eyeline one 
		inst.write(":ACQuire:LTESt ALL")					#turn on limite acquire all channel
		#print inst.query(":ACQuire:RUNTil?")	
		inst.write(":ACQuire:RUNTil WAVeforms,1000")		#set patten frame to 1000
		inst.write(":ACQuire:SSCReen DISK, '%s'"%filename)	#save screen image to disk
		inst.write(":ACQuire:SSCReen:AREA SCReen")			#capture screen area 
		inst.write(":ACQuire:SSCReen:IMAGe INVert")			#remove black background
		time.sleep(16)										#delay for acquire limite
	print "capture screen image over!"
#--------------------------------------------------------------------------#
## Scan parameter of TIA iic register
def Write_Into_Parameter(reg1, reg2 ,reg3, bias):
	print hex(reg1), hex(reg2), hex(reg3)
	if bias == 1:					# open other channel's tail current
		reg_data = [0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x07, reg1, reg2, reg3,\
				    0x07, 0x04, 0x09, 0x00,\
				    0x00, 0x00, 0x00]
	else:
		reg_data = [0x00,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x07, reg1, reg2, reg3,\
				    0x07, 0x72, 0x27, 0x70,\
				    0x00, 0x00, 0x00]
	print "Write into iic register's data:"
	print reg_data
	for i in xrange(len(reg_data)):
		#print i
		iic_write(1, 0x43, 0, i, reg_data[i])
		time.sleep(0.001)
#--------------------------------------------------------------------------#
## Read back paratmeter of TIA iic register
def Read_Back_Parameter():
	iic_read_val = []
	for i in xrange(52):
		iic_read_val += [iic_read(0, 0x43, 1, i)]
	print "Read back iic register's data:" 
	print iic_read_val
#--------------------------------------------------------------------------#
## main function
def main():
	Soc_mode = int(sys.argv[1])			# '1' denotes Jitter mode, '2' denotes Eye/Mask mode
	bias = int(sys.argv[2])				# '1' turn off other channel's tail current, '2' turn on other channel's tail current
	Channel_number = 11					# TIA channel number
	TIACur = 7
	TIAGain = 2
	LACur = 2
	LAGain = 7
	ODAMPL = 7
	PreEm = 0
	for i in xrange(1):	
		#LAGain = i
		reg1 = TIACur << 4 | TIAGain 
		reg2 = LACur << 4 | LAGain 
		reg3 = ODAMPL << 4 | PreEm
		if Soc_mode == 1:
			if bias == 1:
				filename = 'E:\ScreenImage_20180604_Crosstalk\Board1_CH%d_%02x_%02x_%02x_10G_TurnOff_25mV_TurnOffCH10_TurnOnCH12_JITT.bmp'%(Channel_number, reg1, reg2, reg3)
			else:
				filename = 'E:\ScreenImage_20180604_Crosstalk\Board1_CH%d_%02x_%02x_%02x_10G_TurnOn_25mV_TurnOffCH10_TurnOnCH12_JITT.bmp'%(Channel_number, reg1, reg2, reg3)
		else:
			if bias == 1:
				filename = 'E:\ScreenImage_20180604_Crosstalk\Board1_CH%d_%02x_%02x_%02x_10G_TurnOff_25mV_TurnOffCH10_TurnOnCH12_EYE.bmp'%(Channel_number, reg1, reg2, reg3)
			else:
				filename = 'E:\ScreenImage_20180604_Crosstalk\Board1_CH%d_%02x_%02x_%02x_10G_TurnOn_25mV_TurnOffCH10_TurnOnCH12_EYE.bmp'%(Channel_number, reg1, reg2, reg3)
		print filename
		Write_Into_Parameter(reg1, reg2, reg3, bias)
		Read_Back_Parameter()
		time.sleep(1)
		#capture_screen_image(filename, Soc_mode)
		print "Scan Over!\n"
	print "Ok"
#--------------------------------------------------------------------------#
## if statement
if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance	
	main()													#execute main function	
	s.close()												#close socket
