#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os 
import sys
import h5py
import time
import numpy as np
"""@package h5py
This python file is used to test h5py package
"""
## @author WeiZhang
#----------------------------------------------------------------#
def main():
    with open("./h5_output.dat",'w') as infile:
        f = h5py.File('TMS1mmSingleCSAOut1_1.h5','r')           #open .h5 file in read-only mode
        print f.keys()                                          #acquire dataset info 
        data = f['C0'].value                                    #fetch 'C0' dataset value
        print type(f['C0'].value)                                    #fetch 'C0' dataset value
        print len(data[0])
        for i in xrange(len(data[0])):
            if i < 1000000:                                     #fetch 100w data from 'C0' dataset
                infile.write("%.2f\n"%data[0][i])
            else:
                break
        f.close()                                               #close hdf5 file                          
#----------------------------------------------------------------#
if __name__ == "__main__":
    sys.exit(main())
