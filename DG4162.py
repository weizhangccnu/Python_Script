#!/usr/bin/env python
import sys
import visa
import usbtmc
#-----------------------------------------------------------#
def main():
    print "Ok!"
    #instr = usbtmc.Instrument(0x1ab1, 0x0641)
    #instr.timeout = 10
    #print (instr.ask("*IDN?"))
    rm = visa.ResourceManager()
    print(rm.list_resources())
    #inst = rm.open_resource('SRL/dev/ttyS0::INSTR')
    #inst = rm.open_resource('USB0::0x1AB1::0x0641::DG4C143100554::INSTR')
    #inst = rm.open_resource('USB0::0x1AB1::0x0641::DG4E172601737::INSTR')
    #inst = rm.open_resource('USB0::6833::2500::DM3R170500071::0::INSTR')
    #inst = rm.open_resource('USB0::2931::6066::MY54450197::INSTR')
    #print (instr.query("*IDN?"))
    #instr.write("FREQ 100")

#-----------------------------------------------------------#
if __name__ == "__main__":
    sys.exit(main()) 
