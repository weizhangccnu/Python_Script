#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import time
import struct
import socket
from command_interpret import *
'''
@author: Wei Zhang
@date: 2018-01-05
Control module for the Topmetal-S 1mm Electrode single-chip test.
'''
hostname = '192.168.2.3'					#FPGA IP address
port = 1024									#port number
#--------------------------------------------------------------------------#
# Allow combining and disassembling individual registers to/from long integer for I/O
class TMS1mmReg(object):
	## @var _defaultRegMap default register values
	_defaultRegMap = {
		'DAC'	:	[0x75c3, 0x8444, 0x7bbb, 0x7375, 0x86d4, 0xe4b2],	#from DAC1 to DAC6
		'PD'	:	[1, 1, 1, 1],	#from PD1 to PD4, 1 means powered down
		'K'		:	[1, 0, 1, 0, 1, 0, 0, 0, 0, 0],	#from K1 to K10, 1 means clsed (conducting)
		'vref'	:	0x8,
		'vcasp'	:	0x8,
		'vcasn' :	0x8,
		'vbiasp':	0x8,
		'vbiasn':	0x8
	}
	## @var register map local to the class
	_regMap = {}

	def __init__(self):
		self._regMap = copy.deepcopy(self._defaultRegMap)	#deep copy	
	## set each internal DAC's value
	# @param[in] i range from 0-5
	# @param[in] val range from 0-65536
	def set_dac(self, i, val):
		self._regMap['DAC'][i] = 0xffff & val
	## set power down
	# @param[in] i range from 0-3
	# @param[in] onoff 1: powered down 0: powered up
	def set_power_down(self, i, onoff):
		self._regMap['PD'][i] = 0x1 & onoff
	## set analog switch
	# @param[in] i range from 0-9
	# @param[in] onoff 1: closed 0: opened
	def set_k(self, i, onoff):
		self._regMap['K'][i] = 0x1 & onoff
	## set vref voltage
	# @param[in] val 4bit default:0x0100
	def set_vref(self, val):
		self._regMap['vref'] = val & 0xf
	## set vcasp voltage
	# @param[in] val 4bit default:0x0100
	def set_vcasp(self, val):
		self._regMap['vcasp'] = val & 0xf
	## set vcasn voltage
	# @param[in] val 4bit default:0x0100
	def set_vcasn(self, val):
		self._regMap['vcasn'] = val & 0xf
	## set vbiasp voltage
	# @param[in] val 4bit default:0x0100
	def set_vbiasp(self, val):
		self._regMap['vbiasp'] = val & 0xf
	## set vbiasn voltage
	# @param[in] val 4bit default:0x0100
	def set_vbiasn(self, val):
		self._regMap['vbiasn'] = val & 0xf
		
	## Get long-integer variable
	def get_config_vector(self):
		ret = ( self._regMap['vbiasn'] << 126 |
				self._regMap['vbiasp'] << 122 |
				self._regMap['vcasn']  << 118 |
				self._regMap['vcasp']  << 114 |
				self._regMap['vref']   << 110)
		for i in xrange(len(self._regMap['K'])):
			ret |= self._regMap['K'][i] << (len(self._regMap['K']) - i) + 99
		for i in xrange(len(self._regMap['PD'])):
			ret |= self._regMap['PD'][i] << (len(self._regMap['PD']) - i) + 95
		for i in xrange(len(self._regMap['DAC'])):
			ret |= self._regMap['DAC'][i] << (len(self._regMap['DAC'])-1 - i)*16
		return ret

	dac_fit_a = 4.35861E-5
	dac_fit_b = 0.0349427
	def dac_volt2code(self, v):	
		c = int((v - self.dac_fit_b) / self.dac_fit_a)
		if c < 0: 	
			c = 0
		if c > 65535:
			c = 65535
		return c
		
	def dac_code2volt(self, c):
		v = c * self.dac_fit_a + self.dac_fit_b
#--------------------------------------------------------------------------#
## Shift register write and read function
# @param[in] data_to_send 130-bit value to be sent to the external SR
# @param[in] clk_div Clock frequency division factor: (/2**clk_div)
# @return Value stored in the external SR that is read back
# @return valid signal shows that the value stored in external SR is read back
def shift_register_rw(data_to_send, clk_div):
	div_reg = (clk_div & 0x3f) << 130
	data_reg = data_to_send & 0x3ffffffffffffffffffffffffffffffff
	#write in shift register	
	val = div_reg | data_reg
	for i in xrange(9):
		cmd_interpret.write_config_reg(i, (val >> i*16) & 0xffff)
	cmd_interpret.write_pulse_reg(0x0001)            		#generate write puls 
	time.sleep(0.5)											#write data to SR
	# read back	
	ret_all = 0
	for i in xrange(9):
		ret_all |= cmd_interpret.read_status_reg(9-i)
		ret_all = ret_all << 16	
	ret = ret_all & 0x3ffffffffffffffffffffffffffffffff
	valid = (ret_all & (1 << 130)) >> 130
	print ("Return: 0x%0x, valid: %d"%(ret, valid))
	return ret
#--------------------------------------------------------------------------#
## write 32bit data to dac8568
# @param[in] dat write into dac8568's data
def dac8568_write_data(dat):
    cmd_interpret.write_config_reg(0,(0xffff0000&dat)>>16)  #write high word to fifo
    cmd_interpret.write_pulse_reg(0x0002)                   #generate write pulse  
    cmd_interpret.write_config_reg(0,0xffff&dat)            #write low word to fifo
    cmd_interpret.write_pulse_reg(0x0002)                   #generate write pulse
#--------------------------------------------------------------------------#
## config dac8568 via hpdaq FPGA development board
# @param[in] ch choose the dac8568 channel 0-15
# @param[in] data dac8568 write in digital data 0-5V
def config_dac8568(ch, val):
	data = int((val*65535.0)/2.5)                           #convert voltage value to digital code
	dat = 0x58000001                                        #enable internal reference 
	dac8568_write_data(dat)
	dat = 0x5000000a + (ch << 20)+ (data << 4)              #write to selected channel input register
	dac8568_write_data(dat)
	dat = 0x5100000a + (ch << 20) + (data << 4)             #update selected channel register 
	dac8568_write_data(dat)
#--------------------------------------------------------------------------#
def main():
	
	#Config DAC8568 output voltage
	DAC8568_Volt = [1.38, 1.55, 1.45, 1.35, 1.58, 2.68, 1.0, 1.0]
	for i in xrange(8):
		config_dac8568(i, DAC8568_Volt[i])					#DAC8568 Ch1 2.3V
		time.sleep(0.01)
	#enable SDM clock
	#enable 25M sync clock input
	cmd_interpret.write_config_reg(9,0x0003)           		#enable SDM clock
	 
	x2gain = 2
	bufferTest = True
	sdmTest = True

	tms1mmReg = TMS1mmReg()									#define an instance
	tms1mmReg.set_power_down(0, 0)			#AOUT1_CSA power up	
	tms1mmReg.set_power_down(2, 0)			#AOUT1_CSA power up	
	tms1mmReg.set_power_down(3, 0)			#AOUT_BufferX2 power up

	if bufferTest:	
		tms1mmReg.set_k(0, 0)				# 0 - K1 is open, disconnect CSA to output
		tms1mmReg.set_k(1, 1)				# 1 - K2 is closed, allow BufferX2_testIN to inject signal 
		tms1mmReg.set_k(4, 0)				# 4 - K5 is open, disconnect SDM loads 
		tms1mmReg.set_k(6, 1)				# 6 - K7 is closed, BufferX2 output to AOUT_BufferX2 
	if x2gain == 2:
		tms1mmReg.set_k(2, 1)				# 2 - K3 is closed
		tms1mmReg.set_k(3, 0)				# 3 - K4 is open setting gain to X2 
	else:
		tms1mmReg.set_k(2, 0)				# 2 - K3 is	open 
		tms1mmReg.set_k(3, 1)				# 3 - K4 is closed setting gain to X1
	if sdmTest:
		tms1mmReg.set_k(4, 0)				# 4 - K5 is open 
		tms1mmReg.set_k(5, 1)				# 5 - K6 is closed 
	else:
		tms1mmReg.set_k(5, 0)				# 5 - K6 is open
	
	tms1mmReg.set_k(6, 1)					# 6 - K7 is closed, BufferX2 output to AOUT_BufferX2
	tms1mmReg.set_k(7, 1) 					# 7 - K8 is closed, connect CSA out to AOUT1_CSA
	tms1mmReg.set_k(8, 1) 					# 8 - K9 is closed, connect CSA out to AOUT2_CSA
	tms1mmReg.set_dac(0, tms1mmReg.dac_volt2code(1.38))		#VBIASN R45	
	tms1mmReg.set_dac(1, tms1mmReg.dac_volt2code(1.55))		#VBIASP R47	
	tms1mmReg.set_dac(2, tms1mmReg.dac_volt2code(1.45))		#VCSAN  R29	
	tms1mmReg.set_dac(3, tms1mmReg.dac_volt2code(1.35))		#VCSAN  R29	
	tms1mmReg.set_dac(4, tms1mmReg.dac_volt2code(1.58))		#VDIS  	R16	
	tms1mmReg.set_dac(5, tms1mmReg.dac_volt2code(2.68))		#VREF  	R14	
	
	data_to_send = tms1mmReg.get_config_vector()
	print ("Sent: 	0x%0x"% (data_to_send))
	
	div = 7				# shift register write clock divider factor
	shift_register_rw(data_to_send, div)

	print "Ok!"
#--------------------------------------------------------------------------#
if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance	
	main()													#execute main function	
	s.close()												#close socket
