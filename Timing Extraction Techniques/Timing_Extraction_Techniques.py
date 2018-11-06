import os
import sys
import time
import math

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

from sympy.integrals import laplace_transform
from sympy.abc import t, s
'''
Timing extraction techniques simulation: single-threshold, multi-threshold, constant fraction discriminator, waveform sampling
@author: Wei Zhang
@date: Nov 5, 2018
@address: SMU
'''
#======================================================================#
## plot parameters
# hist_bins = 30                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#==========================================================================================================#
## read signal file
def read_signal_file():
    with open("55micron_G_15_Landau/wf_BV300_DV20_W1_H55_SP500_SW490_G15_T250_A0_D0_BW0_C3_L5_GS0.1_BBBW0.7_MIPL0_1.txt", 'r') as signal_file:
        # i = 0
        Data = [[], []]
        for line in signal_file.readlines():
            # i += 1
            # if i >= 2:                                          # read file from third row
                # print i, line
            Data[0] += [float(line.split()[0]) * 1e9]       # change y-axis to ns
            Data[1] += [float(line.split()[1]) * 1e6]       # change x-axis to uV
        return Data
#==========================================================================================================#
## plot signal file
def plot_signal_file(x, y):
    print x
    print y
    plt.plot(x, y, color='b', linewidth=1.5, label='Qin vs TOA')
    # plt.ylim(-30, 5)
    plt.title("Input signal", family="Times New Roman", fontsize=12)
    plt.xlabel("Time [ns]", family="Times New Roman", fontsize=10)
    plt.ylabel("Amplitude [uC]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Input_Signal.png", dpi=fig_dpi)
    # plt.show()
    plt.clf()
#==========================================================================================================#
## main function
def main():
    Data = read_signal_file()
    plot_signal_file(Data[0], Data[1])
    print laplace_transform(t**2, t, s)
    print "Ok!"

#==========================================================================================================#
## if statement
if __name__ == '__main__':
    main()
