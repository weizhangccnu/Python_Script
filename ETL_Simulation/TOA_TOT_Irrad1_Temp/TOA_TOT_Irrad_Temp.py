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
'''
Simulate TOA and TOT varies with Irradiation and Temperature
@author: Wei Zhang
@date: Nov 7, 2018
@address: SMU Dallas, TX
'''
#======================================================================#
## plot parameters
hist_bins = 40                  # histogram bin counts
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
def read_csv_file(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        Data = [[] for i in xrange(6)]
        # print Data
        i = 0
        for row in reader:
            i += 1
            if i > 1:
                for j in xrange(6):
                        Data[j] += [float(row[j * 2 + 1]) * 1e12]
    return Data
#======================================================================#
## fit data with fitting function
# @param[in] toa: toa simulation data, datatype: list
# @param[in] tot: tot simulation data, datatype: list
# @param[in] temp: temperature
# @return popt_toa
def fit_data(toa, tot, irrad, temp):
    popt_toa, pcov_toa = curve_fit(func1, tot, toa)
    plt.plot(tot, toa, 'b.', label='origin data')
    # #print fit
    xmin, xmax = plt.xlim()
    # print "xmin value is: %d"%xmin
    # print "xmax value is: %d"%xmax
    x_ticks = np.arange(xmin-100, xmax+100)

    xtot = np.linspace(xmin, xmax, 1000)
    plt.plot(xtot, func1(xtot, *popt_toa), 'r-', label='fit TOA vs TOT: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt_toa))
    plt.title("TOT vs TOA Irrad=%d  Temp=%s$^{\circ}$C"%(irrad, temp), family="Times New Roman", fontsize=12)
    plt.xlabel("TOT [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("TOA [ps]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.legend(fontsize=8, edgecolor='green')
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("TOT_vs_TOA_Irrad%d_Temp%s.png"%(irrad, temp), dpi=fig_dpi)
    # plt.show()
    plt.clf()
    return popt_toa

#======================================================================#
## TOA fit before correction
def toa_histogram(toa, irrad, temp):
    data = toa                          # toa data in the Excel
    mu, sigma = norm.fit(data)          # fit a normal distribution to the data
    # print mu, sigma

    plt.hist(data, bins=hist_bins, density=True, color='r', label='TOA histogram')
    xmin, xmax = plt.xlim()
    x_ticks = np.arange(xmin-100, xmax+100)

    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: ${\mu}$ = %.2f, ${\sigma}$ = %.2f'%(mu, sigma))


    plt.title("TOA Precision Irrad=%d Temp=%s$^{\circ}$C"%(irrad, temp), family="Times New Roman", fontsize=12)
    plt.xlabel("TOA [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOA_histogram_Irrad%d_Temp%s.png"%(irrad, temp), dpi=fig_dpi)
    plt.clf()
    # plt.show()
#======================================================================#
## TOT fit before correction
def tot_histogram(tot, irrad, temp):
    data = tot                          # tot data in the Excel
    mu, sigma = norm.fit(data)          # fit a normal distribution to the data
    # print mu, sigma
    plt.hist(data, bins=hist_bins, density=True, color='r',label='TOT bin')
    xmin, xmax = plt.xlim()
    x_ticks = np.arange(xmin-100, xmax+100)
    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: ${\mu}$ = %.2f,  ${\sigma}$ = %.2f' % (mu, sigma))

    plt.title("TOT Precision Irrad=%d Temp=%s$^{\circ}$C"%(irrad, temp), family="Times New Roman", fontsize=12)
    plt.xlabel("TOT [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOT_histogram_Irrad%d_Temp%s.png"%(irrad, temp), dpi=fig_dpi)
    # plt.show()
    plt.clf()
#======================================================================#
## time walk correction and fit
# @param[in] popt_toa:
def data_correction(toa, tot, popt_toa, irrad, temp):
    tot_series = pd.Series(tot)
    toa_corrected = func1(tot_series, *popt_toa)       # toa data correction
    data = toa - toa_corrected                  # error distribution
    mu, sigma = norm.fit(data)                  # fit a normal distribution to the data_correction

    plt.hist(data, bins=hist_bins, density=True, color='r', label='hit bin')

    xmin, xmax = plt.xlim()
    x_ticks = np.arange(xmin-100, xmax+100)

    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: $\mu$ = %.2f, $\sigma$ = %.2f' % (mu, sigma))
    plt.title("TOA Precision Corrected Irrad=%d Temp=%s$^{\circ}$C"%(irrad, temp), family="Times New Roman", fontsize=12)
    plt.xlabel("Corrected TOA [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("TOA_Precision_Corrected_Irrad%d_Temp%s.png"%(irrad, temp), dpi=fig_dpi)
    # plt.show()
    plt.clf()
    return sigma
#======================================================================#
## sigma column figure
#@param[in] data: two dimension data
def sigma_column(data):
    n_groups = 3;
    Irrad1 = tuple(data[0])
    Irrad2 = tuple(data[1])
    Irrad3 = tuple(data[2])

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25

    opacity = 0.8
    rects1 = plt.bar(index, Irrad1, bar_width,alpha=opacity, color='b',label='Irrad=1')
    rects2 = plt.bar(index + bar_width, Irrad2, bar_width,alpha=opacity,color='r',label='Irrad=2')
    rects2 = plt.bar(index + 2*bar_width, Irrad3, bar_width,alpha=opacity,color='g',label='Irrad=3')

    plt.xlabel('Temperature', family="Times New Roman", fontsize=8)
    plt.ylabel('TOA Corrected sigma [ps]', family="Times New Roman", fontsize=8)
    plt.title('TOA Corrected sigma distribution', family="Times New Roman", fontsize=12)
    plt.xticks(index + bar_width, ('30$^{\circ}$C', '-20$^{\circ}$C', '-30$^{\circ}$C'))
    plt.ylim(0,65);
    plt.legend(fontsize=8, edgecolor='green')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.tight_layout();
    plt.savefig("Time_Walk.png", dpi=fig_dpi)
    plt.clf()
    # plt.show();

#======================================================================#
## main function
def main():
    filename = ["TOA_TOT_Irrad1_Temp.csv", "TOA_TOT_Irrad2_Temp.csv", "TOA_TOT_Irrad3_Temp.csv"]
    Temp = ["30", "-20", "-30"]
    sigma_data = [[] for i in xrange(len(filename))]
    for irrad in xrange(len(filename)):
        Data = read_csv_file(filename[irrad])
        # print Data
        for temp in xrange(len(Temp)):
            popt_toa = fit_data(Data[temp], Data[temp+3], (irrad+1), Temp[temp])
            toa_histogram(Data[temp], (irrad+1), Temp[temp])
            tot_histogram(Data[temp+3], (irrad+1), Temp[temp])
            sigma_data[irrad] += [data_correction(Data[temp], Data[temp+3], popt_toa, (irrad+1), Temp[temp])]
    print sigma_data
    sigma_column(sigma_data)
    print "OK!"
#======================================================================#
if __name__ == '__main__':
    main()
