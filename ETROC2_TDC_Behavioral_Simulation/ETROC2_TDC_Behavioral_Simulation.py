import os
import sys
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
'''
This script is used to encode the TOA, TOT, and Calibration transfer function of 63 Delay Cells TDC
@author: Wei Zhang
@date: Jan 31, 2019
@address: SMU Dallas, TX
'''
#================================================================================================#
## plot parameters
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#================================================================================================#
## read_csvfile: to read .csv origin simulation data.
def read_csvfile():
    xdata = []
    TOA_Code = []
    TOT_Code = []
    Cal_Code = []
    hitFlag = []
    with open("ETROC2_TDC_testMode=0_polaritySel=1_TOT=6ns_TOA_Scan_20200618.dat", 'r') as infile:
        i = 0
        for line in infile.readlines():
            i += 1
            if i > 20 and int(line.split()[4]) == 1:
                xdata += [i]
                TOA_Code += [int(line.split()[1])]
                TOT_Code += [int(line.split()[2])]
                Cal_Code += [int(line.split()[3])]
                hitFlag += [int(line.split()[4])]

    # TOA Transfer function
    fig, ax = plt.subplots(figsize=(10,6))                                        # Plot TOA transfer function
    ax.plot(xdata, TOA_Code, color='r',marker='X', linewidth=0.2, markersize=0.02, label='TOA Transfer Function')
    plt.title("ETROC2 TDC TOA Transfer Function Step = 1ps", family="Times New Roman", fontsize=12)
    plt.xlabel("TOA Input [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("TOA Code [bins]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    axins = zoomed_inset_axes(ax, 20, loc=7)
    axins.plot(xdata[1000:1180], TOA_Code[1000:1180], color='r',marker='X', linewidth=0.5, markersize=0.8)
    mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.6")
    plt.xticks(family="Times New Roman", fontsize=7)
    plt.yticks(family="Times New Roman", fontsize=7)
    plt.grid(linestyle='-.', linewidth=lw_grid)

    plt.savefig("TOA_Transfer_Function_testMode=0_polaritySel=1_TOT=6ns_1ps.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

    # Cal Code Distribution
    Cal_Code_Min = min(Cal_Code)
    Cal_Code_Max = max(Cal_Code)
    hist_bins = np.arange(Cal_Code_Min-1, Cal_Code_Max+3)

    plt.figure(figsize=(7,5))
    plt.hist(Cal_Code, bins=hist_bins, density=True, color='r', label="hit bin")

    plt.title("Cal Distribution", family="Times New Roman", fontsize=12)
    plt.xlabel("Cal Code", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Cal_Code_Distribution_testMode=0_polaritySel=1_TOT=6ns_1ps.png", dpi=fig_dpi)         # save figure
    plt.clf()

    # TOT Code Distribution
    TOT_Code_Min = min(TOT_Code)
    TOT_Code_Max = max(TOT_Code)
    hist_bins = np.arange(TOT_Code_Min-1, TOT_Code_Max+3)

    plt.figure(figsize=(7,5))
    plt.hist(TOT_Code, bins=hist_bins, density=True, color='r', label="hit bin")

    plt.title("TOT Distribution", family="Times New Roman", fontsize=12)
    plt.xlabel("TOT Code", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOT_Code_Distribution_testMode=0_polaritySel=1_TOT=6ns_1ps.png", dpi=fig_dpi)         # save figure
    plt.clf()

#================================================================================================#
## main function
def main():
    Data = read_csvfile()

#================================================================================================#
if __name__ == '__main__':
    main()
