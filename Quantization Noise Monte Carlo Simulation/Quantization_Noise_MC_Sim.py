import os
import sys
import time
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

'''
TDC Quantization Noise Monte Carlo simulation via Python Script.
@author: Wei Zhang
@date: Jan 14, 2019
@address: SMU Dallas, TX
'''
#==================================================================================#
## plot parameters
hist_bins = 40                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
num = 50000                    # sample count
#==================================================================================#
## sample generator to generate 10000 Guassian data with mu = 0 ps, sigma = 30 ps
def sample_generate():
    mu = 1000                                           # normal distribution mu = 1000ps
    sigma = 30                                          # normal distribution sigam = 30ps
    rand_data = np.random.normal(mu, sigma, num)        # generate data
    rand_data_min = min(rand_data)
    rand_data_max = max(rand_data)
    # print rand_data_min
    # print rand_data_max
    x = np.arange(rand_data_min-20, rand_data_max+20)   # xrange scope
    p = norm.pdf(x, mu, sigma)                          # normal distribution
    # print x, p
    # print rand_data
    plt.hist(rand_data, bins=hist_bins, density=True, color='r', label="hit bin")
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: $\mu$ = %.2f, $\sigma$ = %.2f' % (mu, sigma))

    plt.title("Random Data", family="Times New Roman", fontsize=12)
    plt.xlabel("Time [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Random_Data.png", dpi=fig_dpi)         # save figure
    plt.clf()
    # plt.show()
    # plt.plot(x, p, linewith=1.5, label )
    return rand_data
#==================================================================================#
## unform bin size
# @param_in[] random_data input
def unform_bin_size(rand_data):
    print rand_data
    bin_size = 20                                       # bin size = 20ps
    post_quantization_data = []                         # post quantization data array
    for i in xrange(len(rand_data)):
        digital_code = int(rand_data[i] / bin_size)     # achieve digital code
        # time.sleep(1)
        post_quantization_data += [(digital_code*20)+10]
    print post_quantization_data
    mu, sigma = norm.fit(post_quantization_data)
    print mu, sigma

    post_quan_data = np.random.normal(mu, sigma, num)               # generate data
    post_quan_data_min = min(post_quan_data)
    post_quan_data_max = max(post_quan_data)
    x = np.arange(post_quan_data_min-20, post_quan_data_max+20)     # xrange scope
    p = norm.pdf(x, mu, sigma)                                      # normal distribution

    plt.hist(post_quan_data, bins=hist_bins, density=True, color='r', label="hit bin")
    plt.plot(x, p, color='b', linewidth=1.5, label='Fit results: $\mu$ = %.2f, $\sigma$ = %.2f' % (mu, sigma))

    plt.title("Unform Quantization Data", family="Times New Roman", fontsize=12)
    plt.xlabel("Time [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Unform_Quantization.png", dpi=fig_dpi)         # save figure
    plt.clf()
#==================================================================================#
## unform bin size
# @param_in[] random_data input
def non_unform_bin_size(rand_data):
    print rand_data
    non_unform_sigma = []
    non_unform_mu = []
    for delta in xrange(-20, 21, 1):
        Trf = 20 - delta
        Tfr = 20 + delta
        post_quantization_data = []
        for i in xrange(len(rand_data)):
            xx = int(rand_data[i] / 40)
            yy = rand_data[i] % 40
            if yy > Trf:
                digital_code = xx * 2 + 2
            else:
                digital_code = xx * 2 + 1
            post_quantization_data += [(digital_code*20)-10]
        # print post_quantization_data
        mu, sigma = norm.fit(post_quantization_data)
        non_unform_mu += [mu]
        non_unform_sigma += [sigma]
        print delta,  mu, sigma
    print non_unform_mu
    print non_unform_sigma
    delta_t = np.arange(-20, 21, 1)
    print delta_t

    plt.plot(delta_t, non_unform_mu, color='b', linewidth=1.5, label='non-unform mu')
    plt.title("Non-unform Mu Vs delta T", family="Times New Roman", fontsize=12)
    plt.xlabel("Delta T [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Mu [ps]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Non-unform_mu.png", dpi=fig_dpi)         # save figure
    plt.clf()

    plt.plot(delta_t, non_unform_sigma, color='b', linewidth=1.5, label='non-unform sigma')
    plt.title("Non-unform Sigma Vs delta T", family="Times New Roman", fontsize=12)
    plt.xlabel("Delta T [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("sigma [ps]", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Non-unform_sigma.png", dpi=fig_dpi)         # save figure
    plt.clf()
#==================================================================================#
## main function
def main():
    rand_data = sample_generate()                                   # sample generate
    unform_bin_size(rand_data)                                      # unform bin size
    non_unform_bin_size(rand_data)                                  # non-unform bin size
    print "pass"
#==================================================================================#
## if statement
if __name__ == '__main__':
    main()
