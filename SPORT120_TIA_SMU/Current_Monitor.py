#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import copy
import time
import visa
import datetime
import struct
import socket
from command_interpret import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
'''
@author: Wei Zhang
@date: 2018-03-20
This script is used to monitor power supplly output current for SPORT120 LDD&TIA TID Test.
'''
#--------------------------------------------------------------------------#
## Power supply control and monitor each channel current
## @param[in]: timeslot: fetch monitor current data time slot, unit is second
def monitor_current(timeslot):
    rm = visa.ResourceManager()
    print(rm.list_resources())
    inst1 = rm.open_resource('USB0::0x2A8D::0x1102::MY58041599::0::INSTR')      # top power supply
    inst2 = rm.open_resource('USB0::0x2A8D::0x1102::MY58041595::0::INSTR')      # bottom power supply one
    print(inst1.query("*IDN?"))
    print(inst2.query("*IDN?"))
    inst1.write("*RST")
    inst2.write("*RST")
    time.sleep(1)
    inst1.write("SOURce:VOLTage 1.8,(@1)")                                      # top channel 1
    inst1.write("SOURce:CURRent 0.01,(@1)")

    inst2.write("SOURce:VOLTage 1.2,(@1)")                                      # bottom channel 1
    inst2.write("SOURce:CURRent 0.8,(@1)")
    inst2.write("SOURce:VOLTage 1.2,(@2)")                                      # bottom channel 2
    inst2.write("SOURce:CURRent 0.02,(@2)")
    inst2.write("SOURce:VOLTage 2.5,(@3)")                                      # bottom channel 3
    inst2.write("SOURce:CURRent 0.1,(@3)")

    inst1.write("OUTPut:STATe ON,(@1)")                                         # enable top channel 1
    inst2.write("OUTPut:STATe ON,(@1)")                                         # enable bottom channel 1
    inst2.write("OUTPut:STATe ON,(@2)")                                         # enable bottom channel 2
    inst2.write("OUTPut:STATe ON,(@3)")                                         # enable bottom channel 3

    VDD1V8 = float(inst1.query("MEAS:CURR? CH1"))                               # measure VDD1V8 current
    AVDD1V2 = float(inst2.query("MEAS:CURR? CH1"))                              # measure AVDD1V2 current
    DVDD1V2 = float(inst2.query("MEAS:CURR? CH2"))                              # measure DVDD1V2 current
    DVDD2V5 = float(inst2.query("MEAS:CURR? CH3"))                              # measure DVDD2V5 current
    lasttime = datetime.datetime.now()

    with open("./current_monitor_%s.dat"%(datetime.date.today()), 'a') as infile:
        while True:
            if(datetime.datetime.now() - lasttime > datetime.timedelta(seconds=timeslot)):
                lasttime = datetime.datetime.now()
                AVDD1V2 = float(inst2.query("MEAS:CURR? CH1"))                  # measure AVDD1V2 current
                DVDD1V2 = float(inst2.query("MEAS:CURR? CH2"))                  # measure DVDD1V2 current
                DVDD2V5 = float(inst2.query("MEAS:CURR? CH3"))
                VDD1V8 = float(inst1.query("MEAS:CURR? CH1"))                   # measure VDD1V8 current
                infile.write("%s %6f %6f %6f %6f\n"%(lasttime, AVDD1V2, DVDD1V2, DVDD2V5, VDD1V8))
                print(datetime.datetime.now(), AVDD1V2, DVDD1V2, DVDD2V5, VDD1V8)


#--------------------------------------------------------------------------#
## main function
def main():
    monitor_current(5)
    print("Ok!")
#--------------------------------------------------------------------------#
## if statement
if __name__ == "__main__":
	main()													#execute main function
