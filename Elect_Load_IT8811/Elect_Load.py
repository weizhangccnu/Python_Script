#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time                         #import moudle
import os
import sys
import subprocess
import math
import visa                     #windows instrument driver
#*******************************************************************#
def main():
	rm = visa.ResourceManager()
	print rm.list_resources()
	#instr = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R172501112::INSTR')				#Rigol DM3058E
	instr = rm.open_resource('USB0::0xFFFF::0x8800::017001106771101007::INSTR')			#IT8811
	print instr.query("*IDN?")
	print "OK!"
	instr.close()
#*******************************************************************#
if __name__ == '__main__':
	main()
