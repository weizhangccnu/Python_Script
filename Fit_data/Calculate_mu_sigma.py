#!/usr/bin/env python
import os 
import sys
import time
import numpy as np
from numpy import pi, sqrt, exp, linspace
import scipy.special
from scipy.optimize import curve_fit
import math
#------------------------------------------------------------------------#
## Guassian fitting function
# @para x denotes the self-variable 
# @para a denotes the Amplifer factor
# @para b denotes the mu of Guassian function
# @para c denotes the sigma of Guassian function
def guassian_func(x,a,b,c):                         #guassian fit function
    return a*exp(-(x-b)**2/(2*c**2))

#------------------------------------------------------------------------#
## Read TMS1mmSingleCSAOut1_1hist.dat file and calculate mu and sigma
def Calculate():
    with open("./TMS1mmSingleCSAOut1_1hist.dat",'r') as infile:
        i = 0
        xd = []
        yd = []
        for line in infile.readlines():
            if i > 965005 and i < 965133:
                a = line.split()[0]
                xd += [float(a[:22])]
                yd += [int(line.split()[1])]
            i+=1
        p0 = [5000, 0.968, 1.0]     #the first parameter should be a proper parameter
        mu, sigma = curve_fit(guassian_func, xd, yd, p0)
        print mu

#------------------------------------------------------------------------#
## Main function
def main():
    Calculate()

#------------------------------------------------------------------------#
## Execute main function
if __name__ == "__main__":
    sys.exit(main())
