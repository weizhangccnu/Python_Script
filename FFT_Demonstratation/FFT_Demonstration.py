#!/usr/bin/env python
import sys
import os
from numpy import * 
from math import *
#====================================================================#
def main():
    with open("./fft_result.dat",'w') as infile:
        result_sin = []
        xx = linspace(0, 2*pi, 8, endpoint=False)
        print xx
        yy = []
        for i in xrange(len(xx)):
            yy += [sin(xx[i])]
        
        result_sin = fft.fft(yy)/len(yy)
        print result_sin
        
        xx = linspace(0, 2*pi, 8, endpoint=False)
        print xx
        yy = []
        for i in xrange(len(xx)):
            yy += [cos(xx[i])]
        print fft.fft(yy)/len(yy)
        print abs(fft.fft(yy)/len(yy))
    
        x = arange(0, 2*pi, 2*pi/128)
        y = []
        for i in xrange(len(x)):
            y += [0.3*cos(x[i]) + 0.5*cos(2*x[i] + pi/4) + 0.8*cos(3*x[i] + pi/3)]
        print y
        yf = fft.fft(y)/len(y)
        print yf
        for i in xrange(len(yf)/2+1):
            infile.write("%d %.5f %.5f\n"%(i,abs(yf[i]), angle(yf[i],deg = True)))


#====================================================================#
if __name__ == "__main__":
    sys.exit(main())
