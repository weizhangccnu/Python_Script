import os
import sys
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
'''
This script is used to Calculate TDC measured latency
@author: Wei Zhang
@date: Jan 31, 2019
@address: SMU Dallas, TX
'''
#================================================================================================#
## plot parameters
hist_bins = 40                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#================================================================================================#
def read_csvfile():
    with open("TDC_Measured_Value_5p_nominal.csv", 'rb') as csvfile:
        reader = csv.reader(csvfile)
        Data = [[] for j in xrange(1280)]
        i = 0
        for row in reader:
            i += 1
            if i > 1:
                for col in xrange(len(row)/2):
                    Data[i-2] += [float(row[col*2+1]) > 0.6 and 1 or 0]
    return Data
#================================================================================================#
def counter_decode(Data):
    print Data
    Decode_Data = [[] for j in xrange(len(Data))]
    TDC_Code = []
    for i in xrange(len(Data)):
        # print type(Data[i][1])
        CNT0 = Data[i][0] << 3 | Data[i][1] << 2 | Data[i][2] << 1 | Data[i][3]
        CNT31 = Data[i][4] << 3 | Data[i][5] << 2 | Data[i][6] << 1 | Data[i][7]
        if Data[i][8:].count(1) > 1:
            print Data[i][8:], "Wrong"
        else:
            print Data[i][8:]
        TOA_DEOUT =  63 - Data[i][8:].index(1)
        # print CNT0, CNT31, TOA_DEOUT
        if TOA_DEOUT >= 31:
            TDC_Code += [(((CNT0+1)%16)*63)+TOA_DEOUT]
            cnt = (CNT0+1)%16
        else:
            TDC_Code += [(((CNT31+2)%16)*63)+TOA_DEOUT]
            cnt = (CNT31+2)%16
        # print i,CNT0, CNT31, TOA_DEOUT, cnt, TDC_Code[i]
        Decode_Data[i] += [CNT0, CNT31, TOA_DEOUT, TDC_Code[i]]
        # print Decode_Data[i]
    # print Decode_Data

    # for i in np.arange(0.1, 5.6, 0.05):
    x = []
    for i in np.arange(0.1, 6.5, 0.005):
        x += [float(i)]
    print len(x), len(TDC_Code)
    # plt.plot(x, TDC_Code, color='r',marker='X', linewidth=0.2, markersize=0.02, label='TDC Measured value 63 Delay Cells')
    # plt.title("TDC Measured Value Step = 5ps nominal", family="Times New Roman", fontsize=12)
    # plt.xlabel("Ts_s [ns]", family="Times New Roman", fontsize=10)
    # plt.ylabel("Count [bins]", family="Times New Roman", fontsize=10)
    #
    # plt.xticks(family="Times New Roman", fontsize=8)
    # plt.yticks(family="Times New Roman", fontsize=8)
    # plt.grid(linestyle='-.', linewidth=lw_grid)
    # plt.legend(fontsize=8, edgecolor='green')
    fig, ax = plt.subplots()
    ax.plot(x, TDC_Code, color='r',marker='X', linewidth=0.2, markersize=0.02, label='TDC Measured value 63 Delay Cells')
    plt.title("TDC Measured Value Step = 5ps nominal", family="Times New Roman", fontsize=12)
    plt.xlabel("Ts_s [ns]", family="Times New Roman", fontsize=10)
    plt.ylabel("Count [bins]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')

    axins = zoomed_inset_axes(ax, 20, loc=7)
    axins.plot(x[0:18], TDC_Code[0:18], color='r',marker='X', linewidth=0.5, markersize=0.8Zf)

    mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.6")
    plt.xticks(family="Times New Roman", fontsize=7)
    plt.yticks(family="Times New Roman", fontsize=7)
    plt.grid(linestyle='-.', linewidth=lw_grid)

    # plt.show()
    plt.savefig("TDC_Measured_Value_5ps_nominal.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()


#================================================================================================#
def main():
    Data = read_csvfile()
    Decode_Data = counter_decode(Data)
    # print Decode_Data
    print "OK!"
#================================================================================================#
if __name__ == '__main__':
    main()
