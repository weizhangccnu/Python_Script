#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import copy
import visa
import time
import struct
import socket
import datetime
from command_interpret import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
'''
@author: Wei Zhang
@date: 2018-03-20
This script is used for testing ETROC1 TDC chip. The mianly function of this script is I2C write and read, Ethernet communication, instrument control and so on.
'''
hostname = '192.168.2.3'					#FPGA IP address
port = 1024									#port number
#--------------------------------------------------------------------------#
## plot parameters
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
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
    # post trigger address
    cmd_interpret.write_config_reg(10, 0xffff & post_trigger_addr)
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
    print("sent pulse!")

    cmd_interpret.write_config_reg(0, 0x0001)       # written enable

    write_data_into_ddr3(1, 0x0000000, 0x0100000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop

    time.sleep(1)
    cmd_interpret.write_config_reg(0, 0x0000)       # write enable
    time.sleep(2)
    read_data_from_ddr3(0x0100000)                  # set read begin address

    data_out = []
    ## memoryview usage
    for i in range(30):
        data_out += cmd_interpret.read_data_fifo(60000)           # reading start
    return data_out
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
    cmd_interpret.write_pulse_reg(0x0001)           # reset ddr3 data fifo
    time.sleep(0.01)
    # print(hex(val))
#--------------------------------------------------------------------------#
## IIC read slave device
# @param mode[1:0] : '0'is 1 bytes read or wirte, '1' is 2 bytes read or write, '2' is 3 bytes read or write
# @param slave[7:0]: slave device address
# @param wr: 1-bit '0' is write, '1' is read
# @param reg_addr[7:0] : register address
def iic_read(mode, slave_addr, wr, reg_addr):
    val = mode << 24 | slave_addr << 17 |  0 << 16 | reg_addr << 8 | 0x00	  # write device addr and reg addr
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module

    val = mode << 24 | slave_addr << 17 | wr << 16 | reg_addr << 8 | 0x00	  # write device addr and read one byte
    cmd_interpret.write_config_reg(4, 0xffff & val)
    cmd_interpret.write_config_reg(5, 0xffff & (val>>16))
    time.sleep(0.01)
    cmd_interpret.write_pulse_reg(0x0001)				                      # Sent a pulse to IIC module
    time.sleep(0.01)									                      # delay 10ns then to read data
    return cmd_interpret.read_status_reg(0) & 0xff
#--------------------------------------------------------------------------#
## ddr3 fetching data plot
# @param[in] data: a data list
def data_plot(data):
    plt.plot(data, color='r',marker='X', linewidth=0.2, markersize=0.02, label='DDR3 fetched data')
    plt.title("DDR3 Fetched data plot", family="Times New Roman", fontsize=12)
    plt.xlabel("Point", family="Times New Roman", fontsize=10)
    plt.ylabel("Number", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("DDR3_Fetched_data.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()
#--------------------------------------------------------------------------#
## Scan parameter of LLD register
def Write_Into_Parameter(reg1, reg2):
	print(hex(reg1), hex(reg2))
	reg_data = [0x40, 0x12,\
                0x40, 0x12,\
                0x40, 0x12,\
                0x40, 0x12,\
                0x40, 0x12,\
                0x40, 0x12,\
                0x40, 0x12,\
				0x40, 0x12,\
                0x40, 0x12,\
                reg1, reg2,\
                0x40, 0x12,\
                0x40, 0x12,\
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,\
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
	print("Write into iic register's data:")
	print(reg_data)
	for i in range(len(reg_data)):
		iic_write(1, 0x41, 0, i, reg_data[i])                         # LDD #2 board slave addr = 0x43, #4 board slave addr = 0x41
#--------------------------------------------------------------------------#
## Read back paratmeter of TIA iic register
def Read_Back_Parameter():
	iic_read_val = []
	for j in range(52):
		iic_read_val += [iic_read(0, 0x41, 1, j)]                     # LDD #2 board slave addr = 0x43, #4 board slave addr = 0x41
	print("Read back iic register's data:")
	print(iic_read_val)
#--------------------------------------------------------------------------#
## capture_screen_image
def capture_screen_image(filename):
    rm = visa.ResourceManager()
    print(rm.list_resources())
    inst = rm.open_resource('GPIB1::1::INSTR')              # connect to SOC
    print(inst.query("*IDN?"))                              # Instrument ID
    inst.write("*RST")                                      # reset the OSC
    time.sleep(8)
    # print(inst.query("TIME?"))
    inst.write("ACQuire:SAMPlingmode ET")                   # Acquire samplinng mode : Equivalent Time
    time.sleep(0.01)
    inst.write("TRIGGER:A:EDGE:SOURCE CH2")                 # set tirgger source and edge
    inst.write("HORizontal:MODE:SCAle 2.0E-11")             # set horizontal scale
    inst.write("DISplay:PERSistence INFPersist")
    inst.write("CH1:SCAle 5.0E-2")
    print(inst.query("CH1:SCAle?"))
    inst.write("MEASUREMENT:MEAs1:TYPE FREQUENCY")          # measurement one: frequency
    inst.write("MEASUREMENT:MEAs2:TYPE RISe")               # measurement two: Rising TIME
    inst.write("MEASUREMENT:MEAs3:TYPE FALL")               # measurement three: Falling TIME
    inst.write("MEASUREMENT:MEAs4:TYPE AMPlitude")          # measurement four: Eyediagram amplitude
    inst.write("MEASUREMENT:MEAs5:TYPE PTOP")               # measurement four: Eyediagram Top height
    inst.write("MEASUREMENT:MEAs6:TYPE PBASe")              # measurement four: Eyediagram base height

    inst.write("MEASUrement:MEAS1:STATE ON")                # display frequency measurement results
    inst.write("MEASUrement:MEAS2:STATE ON")                # display rising edge measurement results
    inst.write("MEASUrement:MEAS3:STATE ON")                # display falling edge measurement results
    inst.write("MEASUrement:MEAS4:STATE ON")                # display RMS jitter measurement results
    inst.write("MEASUrement:MEAS5:STATE ON")                # display RMS jitter measurement results
    inst.write("MEASUrement:MEAS6:STATE ON")                # display RMS jitter measurement results
    print(inst.query("MEASUrement:MEAS1:STATE?"))
    time.sleep(40)

    inst.write("EXPort:FORMat PNG")                         # set export image format
    inst.write("EXPort:VIEW FULLSCREEN")                    # view range
    inst.write("EXPort:PALEtte COLOr")                      # palette full color
    inst.write("EXPort:FILEName 'E:\\SPORT120_OSC\\1125\\LDD\\%s.PNG'"%filename)      # file store desitination
    inst.write("EXPort STARt")                              # start exprot image
    print(inst.query("EXPort?"))                            # query export destination

#--------------------------------------------------------------------------#
## main function
def main():
    reg1 = 0x1c
    reg2 = 0x02
    Write_Into_Parameter(reg1, reg2)                        # write I2C register
    Read_Back_Parameter()                                   # read I2C register
    filename = "BRD4_CH3_%s_%s_TurnOFF_10G_400mVpp_1_8Bias_EYE"%(hex(reg1), hex(reg2))
    capture_screen_image(filename)                          # save OSC eyediagram
    print("Ok!")
#--------------------------------------------------------------------------#
## if statement
if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance
	main()													#execute main function
	s.close()												#close socket
