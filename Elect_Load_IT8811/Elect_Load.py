#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time                         #import moudle
import os
import sys
import subprocess
import math
import visa                     #windows instrument driver
'''
PC communicate with IT8811 electronic load via USB on Windows operating system
Electronic load serial number: 13000919
'''
#*******************************************************************#
def main():
	rm = visa.ResourceManager()
	print rm.list_resources()
	#instr = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R172501112::INSTR')				#Rigol DM3058E
	instr = rm.open_resource('USB0::0xFFFF::0x8800::017001106771101007::INSTR')			#IT8811
	print instr.query("*IDN?")
	for i in xrange(32):
		step = i * 0.2
		instr.write("SOURce:CURRent %f"%step)
		time.sleep(1)
		print instr.query(":FETCh:VOLTage:DC?")                                             #Fetch the voltage value
		print instr.query(":FETCh:Current:DC?")                                             #Fetch the voltage value
	instr.close()
	print "OK!"
#*******************************************************************#
if __name__ == '__main__':
	main()
