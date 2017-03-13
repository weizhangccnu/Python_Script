#!/usr/bin/env python
import os
import sys
import visa
import time
#-----------------------------------------------------------#
def main():
    print "Ok!"
    rm = visa.ResourceManager()
    #instr = usbtmc.Instrument(0x1ab1, 0x0641)
    #instr.timeout = 10
    #print (instr.ask("*IDN?"))
    #instr.write("FREQ 100")

#-----------------------------------------------------------#
if __name__ == "__main__":
    sys.exit(main()) 
