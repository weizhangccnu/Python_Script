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
# filename = 'Array_Data_Pixel=15_DAC_P15=409_QSel=6_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=30_B1_1000000_2020-07-01_17-22-24.dat'
# filename = 'Array_Data_Pixel=15_DAC_P15=409_QSel=18_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=30_B1_1000000_2020-07-01_17-23-08.dat'
# filename = 'Array_Data_Pixel=15_DAC_P15=409_QSel=31_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=30_B1_1000000_2020-07-01_17-24-15.dat'

# filename = 'Array_T_Pixel=15_DAC_P15=409_QSel=31_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=100_B1_500000_2020-07-02_16-00-18.dat'
# filename = 'Array_T_Pixel=15_DAC_P15=409_QSel=31_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=100_B1_500000_2020-07-02_16-06-11.dat'
# filename = 'Array_T_Pixel=15_DAC_P15=409_QSel=18_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=100_B1_500000_2020-07-02_16-09-56.dat'
# filename = 'Array_T_Pixel=15_DAC_P15=409_QSel=6_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=100_B1_500000_2020-07-02_16-16-53.dat'
filename = 'Array_T_Pixel=15_DAC_P15=409_QSel=6_CLSel=1_RfSel=3_IBSel=7_TDC_testMode=0_PhaseAdj=150_B1_500000_2020-07-02_16-20-23.dat'
# filename = "123.dat"
# rcParams['font.family'] = "Times New Roman"
#===================================================================================#
def Code_Distribution():
    TOA_Code = []
    TOT_Code = []
    Cal_Code = []
    HitFlag = []
    with open(filename, 'r') as outfile:
        for line in outfile.readlines():
            # print(line.split())
            TOA_Code += [int(line.split()[0])]
            TOT_Code += [int(line.split()[1])]
            Cal_Code += [int(line.split()[2])]
            HitFlag += [int(line.split()[3])]

    TOA_Code_Min = min(TOA_Code)
    TOA_Code_Max = max(TOA_Code)
    print(TOA_Code_Max)
    hist_bins = np.arange(TOA_Code_Min-1.5, TOA_Code_Max+0.5)
    hist_bins1 = np.arange(TOA_Code_Min-1.5, TOA_Code_Max+0.5, 0.1)
    (mu, sigma) = norm.fit(TOA_Code)
    print(mu, sigma)

    fit_data = [sum(list(Counter(TOA_Code).values()))*x for x in mlab.normpdf(hist_bins1, mu, sigma)]
    # print(fit_data)
    plt.figure(figsize=(7,5))
    plt.hist(TOA_Code, bins=hist_bins, density=False, facecolor='g', alpha=0.5, label="TOA Code")
    plt.plot(hist_bins1, fit_data, 'b--', linewidth=2, label="\u03bc=%.3f, \u03c3=%.3f"%(mu, sigma))
    plt.title("ETROC1 Array Full Chain TOA Distribution", family="Times New Roman", fontsize=12)
    plt.xlabel("TOA Code", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOA_Code_Distribution_%s.pdf"%filename.split('B1')[0], dpi=fig_dpi)         # save figure
    plt.clf()

    TOT_Code_Min = min(TOT_Code)
    TOT_Code_Max = max(TOT_Code)
    hist_bins = np.arange(TOT_Code_Min-1.5, TOT_Code_Max+0.5)

    hist_bins1 = np.arange(TOT_Code_Min-1.5, TOT_Code_Max+0.5, 0.1)
    (mu, sigma) = norm.fit(TOT_Code)
    print(mu, sigma)

    fit_data = [sum(list(Counter(TOT_Code).values()))*x for x in mlab.normpdf(hist_bins1, mu, sigma)]

    plt.figure(figsize=(7,5))
    plt.hist(TOT_Code, bins=hist_bins, density=False, facecolor='g', alpha=0.5, label="TOT Code")
    plt.plot(hist_bins1, fit_data, 'b--', linewidth=2, label="\u03bc=%.3f, \u03c3=%.3f"%(mu, sigma))
    plt.title("ETROC1 Array Full Chain TOT Distribution", family="Times New Roman", fontsize=12)
    plt.xlabel("TOT Code", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOT_Code_Distribution_%s.pdf"%filename.split('B1')[0], dpi=fig_dpi)         # save figure
    plt.clf()

    Cal_Code_Min = min(Cal_Code)
    Cal_Code_Max = max(Cal_Code)
    hist_bins = np.arange(Cal_Code_Min-1.5, Cal_Code_Max+0.5)

    hist_bins1 = np.arange(Cal_Code_Min-1.5, Cal_Code_Max+0.5, 0.1)
    (mu, sigma) = norm.fit(Cal_Code)
    print(mu, sigma)

    fit_data = [sum(list(Counter(Cal_Code).values()))*x for x in mlab.normpdf(hist_bins1, mu, sigma)]

    plt.figure(figsize=(7,5))
    plt.hist(Cal_Code, bins=hist_bins, density=False, facecolor='g', alpha=0.5, label="Cal Code")
    plt.plot(hist_bins1, fit_data, 'b--', linewidth=2, label="\u03bc=%.3f, \u03c3=%.3f"%(mu, sigma))
    plt.title("ETROC1 Array Full Chain Cal Distribution", family="Times New Roman", fontsize=12)
    plt.xlabel("Cal Code", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Cal_Code_Distribution_%s.pdf"%filename.split('B1')[0], dpi=fig_dpi)         # save figure
    plt.clf()
#===================================================================================#
def main():
    print("OK!")
    # TDC_Converted_Data_Plot()
    Code_Distribution()
#===================================================================================#
if __name__ == '__main__':
    main()
