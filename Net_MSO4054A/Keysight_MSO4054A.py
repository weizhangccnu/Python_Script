#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import h5py
import socket
'''
@author: WeiZhang
@date: 2018-01-09
remote control Keysight MSO-X 4054A oscillioscope via LXI protocol
'''
hostname = '192.168.2.5' 			#OSC ip address
port = 5025                         #Keysight instrutment ID
#-------------------------------------------------------------------------#
## main function
def main():
    s.send("*IDN?;")
    print "Instrument ID: %s"% s.recv(100)                      #query instrument ID

    Channel_ONOFF = int(sys.argv[1], 16)                        #receive open channel value
    print "Opned Channels: 0x%0x"%Channel_ONOFF
    
    for i in xrange(4):                                         #Open display channels
        if Channel_ONOFF & 0x1 == 1:
            s.send(":CHANnel%s:DISPlay ON;"%(i+1))
            time.sleep(0.1)
        Channel_ONOFF = Channel_ONOFF >> 1                      #open each channel repectively

    s.send(":TIMebase:RANGe?;")                                 #acquire x-axis time range
    time_range = float(s.recv(50)[1:])
    print "Timebase range: %s"% time_range

    s.send(":Timebase:POSition?;")                              #acquire timebase position
    print "Timebase position: %s"% s.recv(50)[1:]               
    
    s.send(":CHANnel1:RANGe?;")                                 #acquire channel3 y-axis full range
    print "Channel1 vertical full range: %s"% s.recv(50)[1:]
    
    s.send(":CHANnel1:SCALe?;")                                 #acquire channel3 vertical sacle
    print "CHANnel1 Vertical scale: %s"% s.recv(50)[1:]         
        
    s.send(":ACQuire:SRATe?;")                                  #acquire sample rate
    sample_rate = float(s.recv(50)[1:])
    print "Acquire sample rate: %s"% sample_rate
    
    s.send(":ACQuire:TYPE?;")                                   #acquire type 
    print "Acquire type: %s"% s.recv(50)[1:]
    
    total_point = sample_rate * time_range                      #calculate total sample point
    print "Total sample point: %d"% total_point
    
    s.send(":WAVeform:SOURce CHANnel1;")                        #acquire channel 1 source data
    s.send(":WAVeform:FORMat BYTE;")                            #return byte data format
    s.send(":WAVeform:PREamble?;")                              #return byte data format
    print "Waveform preamble: %s"% s.recv(100)[1:]
     
    s.send(":WAVeform:COUNT?;")
    print "Waveform counts: %s"% s.recv(50)[1:]

    print "Ok!"
#-------------------------------------------------------------------------#
if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #establish socket
	s.connect((hostname, port))                                 #connet socket
	main()                                                      #execute main function
	s.close                                                     #close socket

