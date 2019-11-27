import os
import sys
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib import gridspec
#======================================================================#
## plot parameters
hist_bins = 40                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#========================================================================#
def main():
    with open("LifeTest_Opowers.TXT") as infile:                                # read data file
        i = 0
        data = [[] for i in range(25)]
        for lines in infile.readlines():
            if i >= 1:
                for j in range(len(data)):
                    if j == 0:
                        data[0] += [lines.split("\t")[0]]                       # x-axis data
                    else:
                        data[j] += [float(lines.split("\t")[j])]                # y-axis data
            i = i + 1;

    xdata = []
    xdata += [0]                                                                                    # the start time is the 0 day
    start_time = datetime.datetime.strptime(data[0][0], '%m/%d/%Y %H:%M:%S.%f')                     # convert time to datetime format
    for i in range(len(data[0])):
        if i != 0:
            time_delta = datetime.datetime.strptime(data[0][i], '%m/%d/%Y %H:%M:%S.%f')-start_time  # Calculate time interval
            xdata +=[time_delta.days + time_delta.seconds/(24.0*3600)]                              # time unit is days
    print(xdata)

    markerstyle = ['H', 'h', '*', '^', 'o', 'v', '<', '>', '^', '.']
    colorstyle = ['g', 'b', 'r', 'lime', 'gold', 'm', 'k', 'c', 'y', 'tan', '#554433', '#445566',\
     '#335577', '#553377', '#773355', '#775533', '#557733', '#337755', '#557799', '#559977', '#775599', '#7799aa', '#aabbcc', '#e4ff00']    # plot data colorstyle
    for i in range(len(data)-1):
        if i < 24:
            plt.plot(xdata[::30], data[i+1][::30], color=colorstyle[i%24], marker=markerstyle[i%10], markersize=0.2, linewidth=0.1, label='P%s'%(i+1))
        else:
            plt.plot(xdata[::30], data[i+1][::30], color=colorstyle[i%24], marker=markerstyle[i%10], markersize=0.2, linewidth=0.1, label='V%s'%(i+1-24))
    plt.title("Power Monitor", family="Times New Roman", fontsize=12)
    plt.xlabel("Time [days]", family="Times New Roman", fontsize=10)
    plt.ylabel("Power [dBm]", family="Times New Roman", fontsize=10)
    plt.xlim(0, 125)
    plt.legend(fontsize=5, edgecolor='g')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.minorticks_on()                                                         # open minorticks
    plt.tick_params(which='minor', width=0.5)                                   # set minor ticks style
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("Power_Monitor.png", dpi=fig_dpi, bbox_inches='tight')
    plt.clf()

    print("Ok!")
#=======================================1================================#
if __name__ == '__main__':
    main()
