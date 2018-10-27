import os
import sys
import csv
import time
import numpy as np

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
import matplotlib.font_manager as font_manager

#======================================================================#
#get data * 1e12 to get unit in ps and ease fitting
# toa = df_toatot['toa'] * 1e12
# tot = df_toatot['tot'] * 1e12

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
    with open("TOT_TOA_Rad123.csv", 'rb') as csvfile:
        column_name = ['TOA_TDC (irrad=1) Y', 'TOA_TDC (irrad=2) Y', 'TOA_TDC (irrad=3) Y', 'TOT_TDC (irrad=1) Y', 'TOT_TDC (irrad=2) Y', 'TOT_TDC (irrad=3) Y']
        data = [[] for i in xrange(6)]
        print len(data)
        for i in xrange(len(data)):
            reader = csv.DictReader(csvfile)
            data[i] = [row[column_name[i]] for row in reader]
            print data[i]
#======================================================================#
## fit data with fitting function
# @return popt_toa
def fit_data():
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
## main function
def main():
    read_csv_file()
    # popt_toa = fit_data()               # execute fit_data function
    # toa_histogram()                     # execute toa_histogram function
    # tot_histogram()                     # execute tot_histogram function
    # data_correction(popt_toa)           # execute toa_corrected function
    print "OK!"
#======================================================================#
if __name__ == '__main__':
    main()
