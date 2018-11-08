import os
import sys
import time

import matplotlib.pyplot as plt
from matplotlib import gridspec
from sympy.abc import a, t, x, s
from sympy.integrals.transforms import laplace_transform
'''
Timing extraction techniques simulation: single-threshold, multi-threshold, constant fraction discriminator, waveform sampling
@author: Wei Zhang
@date: Nov 5, 2018
@address: SMU
'''
#======================================================================#
## plot parameters
hist_bins = 40                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution

filepath = "55micron_G_15_Landau\wf_BV300_DV20_W1_H55_SP500_SW490_G15_T250_A0_D0_BW0_C3_L5_GS0.1_BBBW0.7_MIPL0_3.txt"
#===========================================================================================================#
## read_signal_file
def read_signal_file():
    with open(filepath, 'r') as signal_file:
        Data = [[], []]
        for line in signal_file.readlines():
            Data[0] += [float(line.split()[0]) * 1e9]
            Data[1] += [float(line.split()[1]) * 1e6]
        return Data
#===========================================================================================================#
## plot_signal_file
#@param[in] x: x-axis data
#@param[in] y: y-axis data
def plot_signal_file(x, y):
    plt.plot(x, y, 'r-', linewidth=0.5, label='Sensor output signal')
    plt.title("Sensor Output Signal", family="Times New Roman", fontsize=12)
    plt.xlabel("Time [ns]", family="Times New Roman", fontsize=10)
    plt.ylabel("Current [uA]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.legend(fontsize=8, edgecolor='green')
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("Sensor_output_signal.png", dpi=fig_dpi)
    # plt.show()
    plt.clf()
#===========================================================================================================#
## using Laplace transfer to calculate Vout(s) of Pre-Amplifier
##   Vout(s)                                          RL*(RF * gm -1)
##   -------  = H(s) = -------------------------------------------------------------------------------
##    Iin(S)            S**2 * RF * RL * Cin * CL + S * (RF * Cin + RL * CL + RL * Cin) + 1 - gm * RL
##  first step: calculate h(t) via laplace_inversetransfer
##  second step: calculate convolution between h(t) and  Iin(t) : Vout(t) = Iin(t) (x) h(t)
def preamp_output():
    pass
#===========================================================================================================#
## main function
def main():
    data = read_signal_file()
    print data
    plot_signal_file(data[0], data[1])
    print "Ok!"
#===========================================================================================================#
## if statement
if __name__ == '__main__':
    main()
