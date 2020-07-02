#!/usr/bin/env python3
import os
import sys
import time
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from matplotlib import gridspec
'''
FFT based measurements are subject to errors from an effect known as leakage
@author: Wei Zhang
@date: Nov 15, 2018
@address: SMU
'''
#======================================================================#
## plot parameters
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#===================================================================================#
def FFT_Windows():
    N = 800                 # Number of sample points
    T = 1.0 / 800
    x = np.linspace(0.0, N*T, N)
    y = np.sin(50.0 * 2.0 * np.pi * x)
    print(x, y)
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
    print(gs)
    plt.subplot(gs[0])
    plt.plot(x, y, color='r', linewidth=1.0, label='Sin wave')
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time [s]", family="Times New Roman", fontsize=10)
    plt.ylabel("Volt [V]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0 * T), N//2)
    print(len(xf))

    plt.subplot(gs[2])
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N//2]), color='r', linewidth=1.0, label='FFT')
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Freqency [Hz]", family="Times New Roman", fontsize=10)
    plt.ylabel("Volt [V]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    w = np.hanning(N)

    plt.subplot(gs[1])
    plt.plot(x, y*w, color='g', linewidth=1.0, label='Hanning window')
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Time [s]", family="Times New Roman", fontsize=10)
    plt.ylabel("Volt [V]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    # xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    ywf = fft(w*y)
    plt.subplot(gs[3])
    plt.plot(xf, 2.0 / N * np.abs(ywf[0:N//2]), color='g', linewidth=1.0, label='FFT add Window')
    plt.ylim(-1.5, 1.5)
    plt.xlabel("Freqency [Hz]", family="Times New Roman", fontsize=10)
    plt.ylabel("Volt [V]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.99, top=0.99, wspace=0.25, hspace=0.25)
    plt.savefig("FFT_Windows.pdf", dpi=fig_dpi)
    #plt.show()

#===================================================================================#
def main():
    FFT_Windows()
    print("Ok!")
#===================================================================================#
if __name__ == '__main__':
    main()
