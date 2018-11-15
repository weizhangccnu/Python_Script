import os
import sys
import csv
import time
import numpy as np

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.optimize import curve_fit
from scipy.stats import norm
import matplotlib.font_manager as font_manager

#======================================================================#
## plot parameters
hist_bins = 30                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#======================================================================#

## fitting function f(x) = a + b * (x**1) + c * (x**2) + d * (x**3)
# @param[in] x: self-variable
# @param[in] a: factor for x**0
# @param[in] b: factor for x**1
# @param[in] c: factor for x**2
# @param[in] d: factor for x**3
def func1(x, a, b, c, d):
    return a + b*(x**1) + c*(x**2) + d*(x**3)
#======================================================================#
## read .csv file contents
def read_csv_file():
    with open("TOA_TOT_Vin_20181102.csv", 'rb') as csvfile:
        reader = csv.reader(csvfile)
        Data = [[] for i in xrange(4)]
        print Data
        i = 0
        for row in reader:
            print row
            i += 1
            if i > 3:
                for j in xrange(4):
                    if j % 2 == 0:
                        Data[j] += [float(row[j])* 1e15]
                    else:
                        Data[j] += [float(row[j]) * 1e12]
    return Data
#======================================================================#
## fit data with fitting function
# @param[in] toa: toa simulation data, datatype: list
# @param[in] tot: tot simulation data, datatype: list
# @return popt_toa
def fit_data(toa, tot):
    popt_toa, pcov_toa = curve_fit(func1, tot, toa)
    plt.plot(tot, toa, 'b.', label='origin data')
    # #print fit
    xmin, xmax = plt.xlim()
    print "xmin value is: %d"%xmin
    print "xmax value is: %d"%xmax
    x_ticks = np.arange(xmin-100, xmax+100)

    xtot = np.linspace(xmin, xmax, 1000)
    plt.plot(xtot, func1(xtot, *popt_toa), 'r-', label='fit TOA vs TOT: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt_toa))
    # #ax1.plot(xtot, func1(xtot, *popt_toa), 'r-', label='fit TOA vs TOT: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f, e=%5.3f, f=%5.3f' % tuple(popt_toa))
    plt.title("TOT vs TOA", family="Times New Roman", fontsize=12)
    plt.xlabel("TOT [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("TOA [ps]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.legend(fontsize=8, edgecolor='green')
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("TOT_vs_TOA.png", dpi=fig_dpi)
    # plt.show()
    plt.clf()
    return popt_toa

#======================================================================#
## TOA fit before correction
def toa_histogram():
    data = toa                          # toa data in the Excel
    mu, sigma = norm.fit(data)          # fit a normal distribution to the data
    print mu, sigma

    plt.hist(data, bins=hist_bins, density=True, color='r', label='TOA histogram')
    xmin, xmax = plt.xlim()
    x_ticks = np.arange(xmin-100, xmax+100)

    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: ${\mu}$ = %.2f, ${\sigma}$ = %.2f'%(mu, sigma))


    plt.title("TOA Precision", family="Times New Roman", fontsize=12)
    plt.xlabel("TOA [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOA_histogram.png", dpi=fig_dpi)
    plt.clf()
    # plt.show()
#======================================================================#
## TOT fit before correction
def tot_histogram():
    data = tot                          # tot data in the Excel
    mu, sigma = norm.fit(data)          # fit a normal distribution to the data
    print mu, sigma
    plt.hist(data, bins=hist_bins, density=True, color='r',label='TOT bin')
    xmin, xmax = plt.xlim()
    x_ticks = np.arange(xmin-100, xmax+100)
    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: ${\mu}$ = %.2f,  ${\sigma}$ = %.2f' % (mu, sigma))

    plt.title("TOT Precision", family="Times New Roman", fontsize=12)
    plt.xlabel("TOT [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOT_histogram.png", dpi=fig_dpi)
    # plt.show()
    plt.clf()
#======================================================================#
## time walk correction and fit
# @param[in] popt_toa:
def data_correction(popt_toa):
    toa_corrected = func1(tot, *popt_toa)       # toa data correction
    data = toa - toa_corrected                  # error distribution
    mu, sigma = norm.fit(data)                  # fit a normal distribution to the data_correction

    plt.hist(data, bins=hist_bins, density=True, color='r', label='hit bin')

    xmin, xmax = plt.xlim()
    x_ticks = np.arange(xmin-100, xmax+100)

    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: $\mu$ = %.2f, $\sigma$ = %.2f' % (mu, sigma))
    plt.title("TOA Precision Corrected", family="Times New Roman", fontsize=12)
    plt.xlabel("Corrected TOA [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOA_Precision_Corrected.png", dpi=fig_dpi)
    # plt.show()
    plt.clf()
#======================================================================#
def plot_TOA_Vin(vin, toa):
    plt.plot(vin, toa, color='b', linewidth=1.5, label='Qin vs TOA')
    plt.title("Qin vs TOA", family="Times New Roman", fontsize=12)
    plt.xlabel("Qin [fC]", family="Times New Roman", fontsize=10)
    plt.ylabel("TOA [ps]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Vin_TOA.png", dpi=fig_dpi)
    # plt.show()
    plt.clf()
#======================================================================#
def plot_TOA_TOT(toa, tot):
    popt_toa, pcov_toa = curve_fit(func1, tot, toa)
    plt.plot(tot, toa, 'b.', label='origin data')
    # #print fit
    xmin, xmax = plt.xlim()
    print "xmin value is: %d"%xmin
    print "xmax value is: %d"%xmax
    x_ticks = np.arange(xmin-100, xmax+100)

    xtot = np.linspace(xmin, xmax, 1000)
    plt.plot(xtot, func1(xtot, *popt_toa), 'r-', label='fit TOA vs TOT: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt_toa))
    # #ax1.plot(xtot, func1(xtot, *popt_toa), 'r-', label='fit TOA vs TOT: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f, e=%5.3f, f=%5.3f' % tuple(popt_toa))
    plt.title("TOT vs TOA", family="Times New Roman", fontsize=12)
    plt.xlabel("TOT [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("TOA [ps]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.legend(fontsize=8, edgecolor='green')
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("TOT_vs_TOA.png", dpi=fig_dpi)
    plt.clf()
    return popt_toa
#======================================================================#
def plot_TOA_Residu(vin, toa, tot):
    popt_toa, pcov_toa = curve_fit(func1, tot, toa)
    tot_series = pd.Series(tot)
    toa_corrected = func1(tot_series, *popt_toa)                                # toa data correction
    data = toa - toa_corrected                                                  # error distribution
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 2])
    print gs
    plt.subplot(gs[0])                                                          # multiplot two row one column
    plt.plot(vin, data, color='r', linewidth=1.0, label='TOA Resudial')
    plt.title("Time Walk Residual", family="Times New Roman", fontsize=12)
    # plt.xlabel("Qin [fC]", family="Times New Roman", fontsize=10)
    plt.ylim(-30, 30)
    plt.ylabel("Corrected TOA [ps]", family="Times New Roman", fontsize=10)
    plt.xticks(family="Times New Roman", fontsize=8)
    # plt.xticks([])
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    # plt.savefig("TOA_Residu.png", dpi=fig_dpi)

    plt.subplot(gs[1])
    plt.plot(vin, toa, color='b', linewidth=1.0, label='TOA vs Qin')
    # plt.title("Time Walk Residual", family="Times New Roman", fontsize=12)
    plt.xlabel("Qin [fC]", family="Times New Roman", fontsize=10)
    plt.ylabel("TOA [ps]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.02)
    # plt.show()
    plt.savefig("TOA_Residu.png", dpi=fig_dpi)
    # plt.clf()

#======================================================================#
## main function
def main():

    Data = read_csv_file()
    print Data
    # plot_TOA_Vin(Data[0], Data[1])
    popt_toa = plot_TOA_TOT(Data[1], Data[3])
    plot_TOA_Residu(Data[0], Data[1], Data[3])

    # toa_histogram()                                       # execute toa_histogram function
    # tot_histogram()                                       # execute tot_histogram function
    # data_correction(popt_toa)                             # execute toa_corrected function
    print "OK!"
#======================================================================#
if __name__ == '__main__':
    main()
