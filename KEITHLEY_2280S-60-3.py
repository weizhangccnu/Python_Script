#!/usr/bin/env python
import os 
import sys
import visa
import time
#-------------------------------------------------------------#
## main function 
# @param there is no parameter for main function
def main():
	rm = visa.ResourceManager()
	print rm.list_resources()
	instr1 = rm.open_resource('USB0::0x05E6::0x2280::4106469::INSTR')
	print instr1.query("*IDN?")
	for i in xrange(60):
		print "output voltage %sV"%i
		instr1.write(":VOLTage %s"%i)
		time.sleep(0.5)

	print "OK"
#-------------------------------------------------------------#
## if statement
if __name__ == '__main__':
	main()