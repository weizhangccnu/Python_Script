import os
import sys
import time
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
'''
TDC calibration error simulation and draw errorbar figure
@author: Wei Zhang
@date: March 5, 2019
@address: SMU Dallas, TX
'''
#==================================================================================#
## plot parameters
hist_bins = 2                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#=================================================================================#
## sample data generate
#@param[in] num: generate num data
def sample_generate(num):
    mu = 1000                                           # rising edge mean = 1ns
    sigma = 30                                          # rising edge sigma = 30ps
    rand_data = np.random.normal(mu, sigma, num)        # random random data obey to guassian distribution
    # print rand_data
    # rand_data_min = min(rand_data)
    # rand_data_max = max(rand_data)
    #
    # x = np.arange(rand_data_min-20, rand_data_max+20)
    # p = norm.pdf(x, mu, sigma)
    # plt.hist(rand_data, bins=hist_bins, density=True, color='r', label="hit bin")
    # plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: $\mu$ = %.2f, $\sigma$ = %.2f' % (mu, sigma))
    #
    # plt.title("Random Data", family="Times New Roman", fontsize=12)
    # plt.xlabel("Time [ps]", family="Times New Roman", fontsize=10)
    # plt.ylabel("Density", family="Times New Roman", fontsize=10)
    #
    # plt.xticks(family="Times New Roman", fontsize=8)
    # plt.yticks(family="Times New Roman", fontsize=8)
    # plt.grid(linestyle='-.', linewidth=lw_grid)
    # plt.legend(fontsize=8, edgecolor='green')
    # plt.savefig("Random_Data.png", dpi=fig_dpi)         # save figure
    # plt.clf()
    return rand_data
#=================================================================================#
## calculate bin
def calculate_bin(rand_data, num, average):
    bin_size = 20.0                                         # assume bin size = 20 ps
    clock_period = 3125                                     # 3125 ps clock period
    delta_d = [[0 for m in xrange(10**average)] for k in xrange(num)]
    mean_delta_d = [0 for n in xrange(num)]

    for i in xrange(num):
        for j in xrange(10**average):
            d1 = math.floor(rand_data[i*(10**average)+j] / bin_size)
            d2 = math.floor((rand_data[i*(10**average)+j]+3125) / bin_size)
            delta_d[i][j] = d2 - d1
        # print np.mean(delta_d[i])
        mean_delta_d[i] = np.mean(delta_d[i])
    # print mean_delta_d
    if average == 0:
        # print mean_delta_d
        rand_data_min = min(mean_delta_d)
        rand_data_max = max(mean_delta_d)
        mu, sigma = norm.fit(mean_delta_d)          # fit a normal distribution to the data
        # print mu, sigma
        x = np.arange(rand_data_min-10, rand_data_max+10)
        p = norm.pdf(x, mu, sigma)
        plt.hist(mean_delta_d, bins=2, density=False, color='r', histtype='bar', align='mid', rwidth=10, label="Calibration Code")
        # plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: $\mu$ = %.2f, $\sigma$ = %.2f' % (mu, sigma))

        plt.xlim(154,159)
        plt.title("Calibration Code Histogram", family="Times New Roman", fontsize=12)
        plt.xlabel("Calibration Code", family="Times New Roman", fontsize=10)
        plt.ylabel("Counts", family="Times New Roman", fontsize=10)

        plt.xticks(family="Times New Roman", fontsize=8)
        plt.yticks(family="Times New Roman", fontsize=8)
        plt.grid(linestyle='-.', linewidth=lw_grid)
        plt.legend(fontsize=8, edgecolor='green')
        plt.savefig("Delta_digital_histogram.png", dpi=fig_dpi)         # save figure
        plt.clf()

    mean_delta_digit = np.mean(mean_delta_d)
    var_delta_digit = np.var(mean_delta_d)
    std_delta_digit = np.std(mean_delta_d)

    print "mean of the delta digital of calibration %s"%(mean_delta_digit)
    print "variation of the delta digital of calibration %s"%var_delta_digit
    print "standard deviation of the delta digital of calibration %s"%std_delta_digit

    return mean_delta_digit, std_delta_digit
#=================================================================================#
## main function
def main():
    num = int(sys.argv[1])
    # print num
    x = []
    y = []
    yerr = []
    for i in xrange(5):
        print "sample data number: %s"%num
        print "average time: %s"%(10**i)
        rand_data = sample_generate(num * (10**i))
        # print rand_data
        x += [10**i]
        y += [calculate_bin(rand_data, num, i)[0]]
        yerr += [calculate_bin(rand_data, num, i)[1]]
    print x
    print y
    print yerr

    plt.errorbar(x, y, yerr, color='g', elinewidth=0.8, linewidth=0.5, fmt='--o', ecolor='b', capthick=1, capsize=4, markersize=1.5, marker='X', label='Measured Calibration Code')
    plt.plot(x, [156.25, 156.25, 156.25, 156.25, 156.25], color='r', linewidth=0.8, linestyle='--', label='Real Calibration Code = 156.25')
    plt.title("Calibrated Code vs Average Times", family="Times New Roman", fontsize=12)
    plt.xlabel("Average Times", family="Times New Roman", fontsize=10)
    plt.ylabel("Calibrated Code", family="Times New Roman", fontsize=10)

    plt.xscale('log')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Calibration_Error.png", dpi=fig_dpi)         # save figure
    plt.clf()

    plt.plot(x, yerr, color='r', linewidth=0.5, linestyle='-', markersize=1.5, marker='^', label='Standard deviation')
    plt.axvline(500, 0.01, 0.7, color='b', linestyle='-.', linewidth=0.8, label='0.5 LSB vertical line')
    plt.axvline(6500, 0.01, 0.7, color='b', linestyle=':', linewidth=0.8, label='0.2 LSB vertical line')
    plt.axvline(11000, 0.01, 0.7, color='b', linestyle='--', linewidth=0.8, label='0.1 LSB vertical line')

    plt.title("Standard Deviation vs Average Times", family="Times New Roman", fontsize=12)
    plt.xlabel("Average Times", family="Times New Roman", fontsize=10)
    plt.ylabel("Standard Deviation of Calibration Code", family="Times New Roman", fontsize=10)

    # plt.ylim(0, 0.6)
    plt.xscale('log')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Standard Deviation.png", dpi=fig_dpi)         # save figure
    plt.clf()
    print "Ok!"
#=================================================================================#
## if statement
if __name__ == '__main__':
    main()
