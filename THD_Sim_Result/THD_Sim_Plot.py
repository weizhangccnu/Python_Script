import os
import sys
import csv
import time
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data

import matplotlib.pyplot as plt
from matplotlib import gridspec
'''
Statistics Analog Buffer's THD under all corners
Note that there is no window function in DFT so we must choose interger period of input signal waveform
@author: Wei Zhang
@date: Nov 20, 2018
@address: SMU Dallas, TX.
'''
# cvs_filename = "THD_nominal.csv"
#======================================================================#
## plot parameters
hist_bins = 40                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#==========================================================================#
## read .csv file contents
def read_csv_file(filename):
    print filename
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        Data = [[] for i in xrange(12)]
        # print Data
        i = 0
        for row in reader:
            i += 1
            if i > 1:
                for col in xrange(12):
                    Data[col] += [float(row[col*2+1])]
    return Data
#==========================================================================#
## THD plot
def thd_plot(Data, figurename):
    x = [5, 10, 15, 20, 30, 50, 70, 100]
    print Data[0]
    print Data[1]
    print Data[9]
    markerstyle = ['H', 'h', '*', '^', 'o', 'v', '<', '>', '^', '.' ]
    colorstyle = ['g', 'b', 'r', 'lime', 'gold', 'm', 'k', 'c', 'y', 'tan']
    Freq = [50, 70, 100, 200, 300, 400, 500, 600, 700, 800, 900]
    for i in xrange(len(Data)-5):
        plt.plot(x, Data[i], color=colorstyle[i], marker=markerstyle[i], markersize=2, linewidth=0.8, label='Frequency = %sMHz'%Freq[i])
    plt.title("Analog Buffer THD Distribution  %s"%figurename, family="Times New Roman", fontsize=12)
    plt.xlabel("Sin Waveform Amplitude [mV]", family="Times New Roman", fontsize=10)
    plt.ylabel("THD [%]", family="Times New Roman", fontsize=10)
    # plt.ylim(0, 16, 1)
    plt.legend(fontsize=7, edgecolor='g')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.minorticks_on()                                                         # open minorticks
    plt.tick_params(which='minor', width=0.5)                                   # set minor ticks style
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("THD_Distribution_%s.png"%figurename, dpi=fig_dpi, bbox_inches='tight')
    plt.clf()
    # plt.show()
#==========================================================================#
def main():
    cvs_filename = ["THD_nominal.csv", "THD_ss-45.csv", "THD_ss-20.csv", "THD_ss55.csv", "THD_tt-45.csv", "THD_tt-20.csv", "THD_tt55.csv", "THD_ff-45.csv", "THD_ff-20.csv", "THD_ff55.csv"]
    figurename = ["nominal", "ss-45", "ss-20", "ss55", "tt-45", "tt-20", "tt55", "ff-45", "ff-20", "ff55"]
    for i in xrange(len(cvs_filename)):
        Data = read_csv_file(cvs_filename[i])
        print Data
        thd_plot(Data, figurename[i])
    print "Ok!"
#==========================================================================#
if __name__ == '__main__':
    main()
