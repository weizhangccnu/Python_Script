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
    with open("Delay_Cells_63_TOA_TOT_Tap31_1ps.csv", 'rb') as csvfile:
        reader = csv.reader(csvfile)
        Data = [[] for j in xrange(3600-1)]
        i = 0
        for row in reader:
            i += 1
            if i > 1:
                for col in xrange(len(row)/2):
                    Data[i-2] += [float(row[col*2+1]) > 0.6 and 1 or 0]
    return Data
#================================================================================================#
## TOARaw_Transfer_Function: Encode TOA Raw data to 10-bit binary code.
#@param[in]: Data: TOA, TOT, and Calibration simulation data.
def TOARaw_Transfer_Function(Data):
    TOA_codeReg = []
    for i in xrange(len(Data)):                                     # fetch TOA Raw data
        if Data[i][3:66].count(1) > 1:
            print Data[i][3:66].index(1), "Wrong"
        else:
            TOARaw = Data[i][3:66].index(1)
        TOACntA = Data[i][68]<<2 | Data[i][67]<<1 | Data[i][66]     # TOA Counter A number
        TOACntB = Data[i][71]<<2 | Data[i][70]<<1 | Data[i][69]     # TOT Counter B number
        if Data[i][0] == 1:                                         # TOARawdata[62] = 1; How to choose CounterA and CounterB
            TOA_Code = ((TOACntB)<<1 | 0) * 63 + TOARaw + 1
        else:                                                       # TOARawdata[62] = 0;
            TOA_Code = (((TOACntA-1)<<1) | 1) * 63 + TOARaw + 1
        # print
        # print Data[i][0:1], TOARaw, TOACntA, TOACntB, TOA_Code
        TOA_codeReg += [TOA_Code]
    print len(TOA_codeReg)
    x = []
    for i in np.arange(0.4, 3.999, 0.001):
        x += [float(i)]
    print len(x)

    fig, ax = plt.subplots()                                        # Plot TOA transfer function
    ax.plot(x, TOA_codeReg, color='r',marker='X', linewidth=0.2, markersize=0.02, label='TOA Transfer Function')
    plt.title("63 Delay Cells TDC TOA Transfer Function Step = 1ps nominal", family="Times New Roman", fontsize=12)
    plt.xlabel("TOA_CK [ns]", family="Times New Roman", fontsize=10)
    plt.ylabel("Digital Code [bins]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    axins = zoomed_inset_axes(ax, 20, loc=7)
    axins.plot(x[1000:1050], TOA_codeReg[1000:1050], color='r',marker='X', linewidth=0.5, markersize=0.8)
    mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.6")
    plt.xticks(family="Times New Roman", fontsize=7)
    plt.yticks(family="Times New Roman", fontsize=7)
    plt.grid(linestyle='-.', linewidth=lw_grid)

    plt.savefig("TOA_Transfer_Function_1ps_nominal.pdf", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()
#================================================================================================#
## TOTRaw_Transfer_Function: Encode TOT Raw data to 9-bit binary code. 
#@param[in]: Data: TOA, TOT, and Calibration simulation data.
def TOTRaw_Transfer_Function(Data):
    TOT_codeReg = []
    for i in xrange(len(Data)):
        if Data[i][72:104].count(1) > 1:                            # Get TOT Raw data
            print Data[i][72:104].index(1), "Wrong"
        else:
            TOTRaw = Data[i][72:104].index(1)
        TOTCntA = Data[i][106]<<2 | Data[i][105]<<1 | Data[i][104]  # TOT Counter A number
        TOTCntB = Data[i][109]<<2 | Data[i][108]<<1 | Data[i][107]  # TOT Counter B number
        if TOTRaw == 31:                                            # TOTRawdata = 31
            if Data[i][1] == 0:                                     # TOTRaw[31] = 0
                TOT_Code = ((TOTCntB)<<1 | 0) * 32 + TOTRaw + 1
            else:                                                   # TOTRaw[31] = 1
                TOT_Code = ((TOTCntA-1)<<1 | 1) * 32 + TOTRaw + 1
        else:
            if Data[i][1] == 1:
                TOT_Code = ((TOTCntB)<<1 | 0) * 32 + TOTRaw + 1
            else:
                TOT_Code = (((TOTCntA-1)<<1) | 1) * 32 + TOTRaw + 1
        TOT_codeReg += [TOT_Code]
        # print Data[i][1], TOTRaw, TOTCntA, TOTCntB, TOT_Code
        # print Data[i][1], Data[i][72:104], Data[i][72:104].index(1), Data[i][104:107], Data[i][107:110]
    x = []
    for i in np.arange(0.4, 3.999, 0.001):
        x += [float(i)]
    print len(x)

    fig, ax = plt.subplots()                                        # Plot TOT transfer function
    ax.plot(x, TOT_codeReg, color='r',marker='X', linewidth=0.2, markersize=0.02, label='TOT Transfer Function')
    plt.title("63 Delay Cells TDC TOT Transfer Function Step = 1ps nominal", family="Times New Roman", fontsize=12)
    plt.xlabel("TOT_CK [ns]", family="Times New Roman", fontsize=10)
    plt.ylabel("Digital Code [bins]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    axins = zoomed_inset_axes(ax, 10, loc=7)
    axins.plot(x[1100:1200], TOT_codeReg[1100:1200], color='r',marker='X', linewidth=0.5, markersize=0.8)
    mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.6")
    plt.xticks(family="Times New Roman", fontsize=7)
    plt.yticks(family="Times New Roman", fontsize=7)
    plt.grid(linestyle='-.', linewidth=lw_grid)

    plt.savefig("TOT_Transfer_Function_1ps_nominal.pdf", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

#================================================================================================#
## CalRaw_Transfer_Function: Encode Calibration Raw data to 10-bit binary code.
#@param[in]: Data: TOA, TOT, and Calibration simulation data.
def CalRaw_Transfer_Function(Data):
    Cal_codeReg = []
    for i in xrange(len(Data)):
        if Data[i][110:173].count(1) > 1:
            print Data[i][110:173].index(1), "Wrong"
        else:
            CalRaw = Data[i][110:173].index(1)
        CalCntA = Data[i][175]<<2 | Data[i][174]<<1 | Data[i][173]
        CalCntB = Data[i][178]<<2 | Data[i][177]<<1 | Data[i][176]
        if Data[i][2] == 1:
            Cal_Code = ((CalCntB)<<1 | 0) * 63 + CalRaw + 1
        else:
            Cal_Code = (((CalCntA-1)<<1) | 1) * 63 + CalRaw + 1
        # print
        # print Data[i][2], CalRaw, CalCntA, CalCntB, Cal_Code
        Cal_codeReg += [Cal_Code]
        # print Data[i][2], Data[i][110:173], Data[i][173:176], Data[i][176:179]
    print len(Cal_codeReg)
    x = []
    for i in np.arange(0.4, 3.999, 0.001):
        x += [float(i)]
    print len(x)

    fig, ax = plt.subplots()
    ax.plot(x, Cal_codeReg, color='r',marker='X', linewidth=0.2, markersize=0.02, label='Cal Transfer Function')
    plt.title("63 Delay Cells TDC Cal Transfer Function Step = 1ps nominal", family="Times New Roman", fontsize=12)
    plt.xlabel("Latch_CK [ns]", family="Times New Roman", fontsize=10)
    plt.ylabel("Digital Code [bins]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    axins = zoomed_inset_axes(ax, 20, loc=7)
    axins.plot(x[1000:1050], Cal_codeReg[1000:1050], color='r',marker='X', linewidth=0.5, markersize=0.8)
    mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.6")
    plt.xticks(family="Times New Roman", fontsize=7)
    plt.yticks(family="Times New Roman", fontsize=7)
    plt.grid(linestyle='-.', linewidth=lw_grid)

    plt.savefig("Cal_Transfer_Function_1ps_nominal.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()
#================================================================================================#
def main():
    Data = read_csvfile()
    TOARaw_Transfer_Function(Data)
    TOTRaw_Transfer_Function(Data)
    CalRaw_Transfer_Function(Data)
#================================================================================================#
if __name__ == '__main__':
    main()
