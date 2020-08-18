#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import numpy as np
from scipy.stats import norm
from collections import Counter
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib import rcParams
from matplotlib import gridspec
'''
TDC Converted Data Plot
@author: Wei Zhang
@date: January 3, 2020
@address: SMU
'''
#===================================================================================#
## plot parameters
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
lw = 0.8

#===================================================================================#
def Code_Distribution():
    file_list = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            file_list += [os.path.join(root, name)]
    print(file_list)
    Before_TID_Data = [[] for x in range(20)]
    After_TID_Data = [[] for x in range(20)]
    for i in range(len(file_list)):

        # print(file_list[i].split("\\"))
        if file_list[i].split("\\")[1] == "P_F3" and file_list[i].split("\\")[2].split('.')[1]=="TXT":
            with open(file_list[i], 'r') as infile:
                # print(file_list[i])
                file_num = int(file_list[i].split("\\")[2].split('_')[2].split('.')[0])
                for line in infile.readlines():
                    print(file_list[i].split("\\")[2])
                    for j in range(1024):

                        # print(eval(line.split()[j]))
                        Before_TID_Data[file_num] += [eval(line.split()[j])]

        if file_list[i].split("\\")[1] == "P_F3_TID" and file_list[i].split("\\")[2].split('.')[1]=="TXT":
            # print(file_list[i])
            with open(file_list[i], 'r') as infile:
                # print(file_list[i].split("\\")[2].split('data')[1].split('.')[0])
                file_num = int(file_list[i].split("\\")[2].split('data')[1].split('.')[0])
                for line in infile.readlines():
                    print(file_list[i].split("\\")[2])
                    for j in range(1024):

                        # print(eval(line.split()[j]))
                        After_TID_Data[file_num] += [eval(line.split()[j])]
    print(Before_TID_Data[0])
    print(After_TID_Data[0])
    After_TID = []
    Before_TID = []
    for j in range(len(Before_TID_Data[0])):
        Before_TID_SUM = []
        After_TID_SUM = []
        for i in range(len(Before_TID_Data)):
            Before_TID_SUM += [Before_TID_Data[i][j]]
            After_TID_SUM += [After_TID_Data[i][j]]
        Before_TID += [np.mean(Before_TID_SUM)]
        After_TID += [np.mean(After_TID_SUM)]
    print(min(Before_TID), max(Before_TID))
    print(min(After_TID), max(After_TID))
    # print(After_TID)
    xdata = np.arange(0, 1024)
    print(xdata)

    plt.figure(figsize=(5,3))
    plt.plot(xdata, Before_TID, color='r', marker='^', linewidth=0.2, markersize=0.02, label='Before TID')
    plt.plot(xdata, Before_TID, color='b', marker='>', linewidth=0.2, markersize=0.015, label='After TID')

    plt.title("DAC Output", family="Times New Roman", fontsize=12)
    plt.xlabel("Input 10-Bit Data", family="Times New Roman", fontsize=10)
    plt.ylabel("DAC Output [V]", family="Times New Roman", fontsize=10)

    # plt.xscale('log')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("DAC_Transfer_Function.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

    INL_xdata = np.arange(0,1024)
    Before_LSB_Ideal = (max(Before_TID)-min(Before_TID))/1023

    Before_Ideal = np.arange(min(Before_TID), max(Before_TID), (max(Before_TID)-min(Before_TID))/1024)
    After_LSB_Ideal = (max(After_TID)-min(After_TID))/1023
    After_Ideal = np.arange(min(After_TID), max(After_TID), (max(After_TID)-min(After_TID))/1024)

    print(Before_Ideal)
    Before_TID_INL = []
    After_TID_INL = []
    for i in range(len(Before_TID)):
        Before_TID_INL += [((Before_TID[i] - Before_TID[0])/Before_LSB_Ideal)-i]
        After_TID_INL += [((After_TID[i] - After_TID[0])/After_LSB_Ideal)-i]

    plt.figure(figsize=(5,3))
    plt.plot(INL_xdata, Before_TID_INL, color='r', marker='^', linewidth=0.2, markersize=0.02, label='Before TID')
    plt.plot(INL_xdata, After_TID_INL, color='b', marker='>', linewidth=0.2, markersize=0.015, label='After TID')

    plt.title("DAC INL", family="Times New Roman", fontsize=12)
    plt.xlabel("Input 10-Bit Data", family="Times New Roman", fontsize=10)
    plt.ylabel("INL [LSB]", family="Times New Roman", fontsize=10)

    # plt.xscale('log')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("DAC_INL.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

    DNL_xdata = np.arange(0,1023)
    Before_TID_DNL = []
    After_TID_DNL = []
    for i in range(len(Before_TID)-1):
        Before_TID_DNL += [((Before_TID[i+1] - Before_TID[i])/Before_LSB_Ideal)-1]
        After_TID_DNL += [((After_TID[i+1] - After_TID[i])/After_LSB_Ideal)-1]
    plt.figure(figsize=(5,3))
    plt.plot(DNL_xdata, Before_TID_DNL, color='r', marker='^', linewidth=0.2, markersize=0.02, label='Before TID')
    plt.plot(DNL_xdata, After_TID_DNL, color='b', marker='>', linewidth=0.2, markersize=0.015, label='After TID')

    plt.title("DAC DNL", family="Times New Roman", fontsize=12)
    plt.xlabel("Input 10-Bit Data", family="Times New Roman", fontsize=10)
    plt.ylabel("DNL [LSB]", family="Times New Roman", fontsize=10)

    plt.ylim(-0.4, 0.4)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("DAC_DNL.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

    print("Before TDC INL max: %s"%max(Before_TID_INL))
    print("Before TDC INL min: %s"%min(Before_TID_INL))
    print("After TDC INL max: %s"%max(After_TID_INL))
    print("After TDC INL min: %s"%min(After_TID_INL))

    print("Before TDC DNL max: %s"%max(Before_TID_DNL))
    print("Before TDC DNL min: %s"%min(Before_TID_DNL))
    print("After TDC DNL max: %s"%max(After_TID_DNL))
    print("After TDC DNL min: %s"%min(After_TID_DNL))
#===================================================================================#
def main():
    Code_Distribution()
#===================================================================================#
if __name__ == '__main__':
    main()
