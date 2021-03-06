import os
import sys
import time
import math
import random
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib import gridspec
'''
This python script is used to estimate ETROC0 TDC INL and DNL
@author: Wei Zhang
@date: May 5, 2019
@address: SMU dallas, TX
'''
#======================================================================#
## plot parameters
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#=============================================================================#
## time to digital converter function
# @param[in] time_interval: time interval
# @param[in] Tfr time of 63 delay cells
# @param[in] Trf time of 63 delay cells
def time_to_digital(time_interval, Tfr_Delay_Cell, Trf_Delay_Cell):
    sum = 0
    digital_code = 0
    for i in xrange(700):
        Delay_Cell_Time = 0
        if sum <= time_interval:
            digital_code += 1
            if (i/63)%2 == 0:
                if i%2 == 0:
                    Delay_Cell_Time += Tfr_Delay_Cell[i%63]
                else:
                    Delay_Cell_Time += Trf_Delay_Cell[i%63]
            else:
                if i%2 == 0:
                    Delay_Cell_Time += Tfr_Delay_Cell[i%63]
                else:
                    Delay_Cell_Time += Trf_Delay_Cell[i%63]
            sum += Delay_Cell_Time
    return digital_code-1
#=============================================================================#
## digital to time interval converter function
# @param[in] time_interval: time interval
# @param[in] Tfr time of 63 delay cells
# @param[in] Trf time of 63 delay cells
def digital_to_time(digital_code, Tfr_Delay_Cell, Trf_Delay_Cell):
    sum = 0
    Delay_Cell_Time = 0
    for i in xrange(digital_code):
        if (i/63)%2 == 0:
            if i%2 == 0:
                Delay_Cell_Time += Tfr_Delay_Cell[i%63]
            else:
                Delay_Cell_Time += Trf_Delay_Cell[i%63]
        else:
            if i%2 == 0:
                Delay_Cell_Time += Tfr_Delay_Cell[i%63]
            else:
                Delay_Cell_Time += Trf_Delay_Cell[i%63]
    return Delay_Cell_Time
#=============================================================================#
## Ideal transfer function
def Ideal_Transfer_Function(average_bin_size):
    digital_code = []
    sum = 0
    single_digital_code = 0
    time_interval = np.arange(0, 200, 0.1)
    print time_interval
    for j in xrange(len(time_interval)):
        for i in xrange(700):
            if sum <= time_interval[j]:
                single_digital_code += 1
                sum += average_bin_size
        digital_code += [single_digital_code - 1]
    return time_interval, digital_code

#=============================================================================#
## TDC INL Calculate
#@param[in] average_bin_size: calibrated average bin size
#@param[in] Tfr_Delay_Cell: small bin size of 63 delay cell
#@param[in] Trf_Delay_Cell: big bin size of 63 delay cells
def TDC_INL_Calculate(average_bin_size, Tfr_Delay_Cell, Trf_Delay_Cell, filename):
    TDC_INL = []
    digital_code_stop = time_to_digital(12500, Tfr_Delay_Cell, Trf_Delay_Cell)
    digital_code = np.arange(digital_code_stop)
    for i in xrange(1, len(digital_code)):
        TDC_INL += [digital_to_time(digital_code[i], Tfr_Delay_Cell, Trf_Delay_Cell)/average_bin_size - i]

    plt.plot(digital_code[1:], TDC_INL, color='r',marker='X', linewidth=0.5, markersize=0.8, label='TDC_INL')
    plt.title("TDC INL Estimate", family="Times New Roman", fontsize=12)
    plt.xlabel("Digital Code [bins]", family="Times New Roman", fontsize=10)
    plt.ylabel("TDC INL [LSB]", family="Times New Roman", fontsize=10)
    # plt.ylim(-1,1)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.legend(fontsize=8, edgecolor='green')
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("TDC_INL_Estimate_%s.png"%filename, dpi=fig_dpi)
    plt.clf()

#=============================================================================#
## TDC DNL Calculate
#@param[in] average_bin_size: calibrated average bin size
#@param[in] Tfr_Delay_Cell: small bin size of 63 delay cell
#@param[in] Trf_Delay_Cell: big bin size of 63 delay cells
def TDC_DNL_Calculate(average_bin_size, Tfr_Delay_Cell, Trf_Delay_Cell):
    TDC_DNL = []
    digital_code_stop = time_to_digital(12500, Tfr_Delay_Cell, Trf_Delay_Cell)
    digital_code = np.arange(digital_code_stop)
    for i in xrange(1, len(digital_code)-1):
        TDC_DNL += [(digital_to_time(digital_code[i+1], Tfr_Delay_Cell, Trf_Delay_Cell) - digital_to_time(digital_code[i], Tfr_Delay_Cell, Trf_Delay_Cell))/average_bin_size - 1]

    plt.plot(digital_code[1:len(digital_code)-1], TDC_DNL, color='r',marker='X', linewidth=0.5, markersize=0.8, label='TDC_DNL')
    plt.title("TDC DNL Estimate", family="Times New Roman", fontsize=12)
    plt.xlabel("Digital Code [bins]", family="Times New Roman", fontsize=10)
    plt.ylabel("TDC DNL [LSB]", family="Times New Roman", fontsize=10)
    # plt.ylim(-1,1)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.legend(fontsize=8, edgecolor='green')
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("TDC_DNL_Estimate.pdf", dpi=fig_dpi)
    plt.clf()
#=============================================================================#
def square_number(n):
    return n**2
#=============================================================================#
## calibration bin size
#@param[in] num: average times
#@param[in] Tfr_Delay_Cell: small bin size of 63 delay cell
#@param[in] Trf_Delay_Cell: big bin size of 63 delay cells
def calibration_bin_size(num, Tfr_Delay_Cell, Trf_Delay_Cell):
    sigma = 200                                                     # normal distribution sigam = 30ps
    rand_data = []
    for i in xrange(num):
        mu = random.uniform(1, 10) * 1000
        # print mu
        rand_data += [np.random.normal(mu, sigma, 1)]               # generate data
    digital_interval = []
    for i in xrange(num):
        digital_interval += [time_to_digital(rand_data[i]+3125.0, Tfr_Delay_Cell, Trf_Delay_Cell) - time_to_digital(rand_data[i], Tfr_Delay_Cell, Trf_Delay_Cell)]
    # print digital_interval
    square_digital_interval = map(square_number, digital_interval)
    average_bin_size = (np.mean(digital_interval) * 3125.0) / np.mean(square_digital_interval)
    return average_bin_size

#=============================================================================#
## main function
def main():
    ## the Tfr_mu, Tfr_mu and Tfr_sigma, Tfr_sigma are generated from Monte Carlo simulation
    # Tfr_mu = 18.22              # The mu of Tfr is about 18 ps
    # Tfr_sigma = 0.149           # The sigma of Tfr is about 0.149 ps
    #
    # Trf_mu = 21.13              # The mu of Trf is about 21 ps
    # Trf_sigma = 0.2575          # The sigma of Trf is about 0.5 ps
    #
    # # generate 63 delay cell with different Tfr and Trf due to mismatch
    # Tfr_delay_cell = np.random.normal(Tfr_mu, Tfr_sigma, 63)
    # Trf_delay_cell = np.random.normal(Trf_mu, Trf_sigma, 63)

    # print Tfr_delay_cell
    # print Trf_delay_cell
    Tfr_Delay_Cell = [18.42966469, 18.36038465, 18.30923559, 18.16691961, 18.41675559, 18.15583319,
                        18.23623054, 18.32548448, 18.23866809, 18.30838655, 18.04172126, 18.24424936,
                        18.08599614, 18.4435606,  18.13096359, 18.22667424, 18.07868958, 18.31127712,
                        18.17941516, 18.18409195, 18.05209239, 18.19381707, 18.14195912, 18.11836408,
                        18.05571928, 18.33345544, 18.39333308, 18.10830424, 18.13176281, 18.2011696,
                        18.62806081, 18.32711676, 18.30822702, 18.18842511, 18.22309685, 18.17814679,
                        18.05121604, 18.3826321,  18.13831744, 18.08182082, 18.3614019,  18.19914984,
                        18.20949536, 17.99810823, 18.18994782, 18.1305765,  18.46492512, 18.13354387,
                        18.227393,   18.11373014, 17.99304181, 18.08956811, 17.99732559, 18.46184364,
                        18.20897184, 18.35049551, 17.94528359, 18.20967191, 18.40270099, 18.25065476,
                        18.16077381, 18.34613837, 18.27499901]
    Trf_Delay_Cell = [21.06127356, 21.13441314, 21.24407836, 21.31265035, 21.04855227, 21.47494963,
                        20.97962985, 21.59438587, 21.02856291, 21.13798867, 21.41712171, 21.16697003,
                        21.06441552, 21.0466971,  21.04833158, 21.06997816, 21.45734152, 21.22233117,
                        21.07450112, 21.22430591, 21.18298168, 21.03789847, 20.89743861, 21.20097816,
                        20.9551921,  21.09431805, 21.06222212, 21.27141164, 21.10735968, 20.72164184,
                        20.97349199, 21.17295003, 21.44851302, 21.15927505, 21.47535293, 21.40109019,
                        21.35706234, 21.02553518, 20.62996681, 21.40485905, 21.32901722, 21.1335563,
                        20.58115919, 21.30273271, 21.00104917, 21.03537432, 21.09982294, 21.44551851,
                        21.04101435, 21.13719418, 21.41739651, 20.89846598, 20.81686431, 21.19866769,
                        21.02173107, 21.13358564, 21.25680686, 21.0719056,  21.13027417, 21.77255757,
                        20.84063514, 21.28559414, 21.52816637]
    actual_bin_size = (np.mean(Tfr_Delay_Cell) + np.mean(Trf_Delay_Cell))/2.0
    print actual_bin_size

    # digital_interval = calibration_bin_size(200, Tfr_Delay_Cell, Trf_Delay_Cell)
    # print digital_interval
    # plt.hist(digital_interval, bins=[156.5, 157.5, 158.5, 159.5, 160.5], density=False, color='r', label="Calibration digital code")
    # # plt.title("Calibration Code Histogram", family="Times New Roman", fontsize=12)
    # plt.xlabel("Digital Code [bin]", family="Times New Roman", fontsize=10)
    # plt.ylabel("Counts", family="Times New Roman", fontsize=10)
    # plt.xticks(family="Times New Roman", fontsize=8)
    # plt.yticks(family="Times New Roman", fontsize=8)
    # plt.grid(linestyle='-.', linewidth=lw_grid)
    # plt.legend(fontsize=6, edgecolor='green')
    # plt.savefig("Calibration_digital_code_histogram.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    # plt.clf()
    # average_times = [1, 10, 100, 1000, 10000, 100000]
    # for i in xrange(len(average_times)):
    #     average_bin_size = calibration_bin_size(average_times[i], Tfr_Delay_Cell, Trf_Delay_Cell)
    #     print average_times[i], average_bin_size - actual_bin_size
    #     TDC_INL_Calculate(average_bin_size, Tfr_Delay_Cell, Trf_Delay_Cell, average_times[i])
    average_times = [1, 10, 100, 1000]
    average_bin = [[] for k in xrange(len(average_times))]
    # print average_bin
    for j in xrange(100):
        for i in xrange(len(average_times)):
            average_bin_size = calibration_bin_size(average_times[i], Tfr_Delay_Cell, Trf_Delay_Cell)
            average_bin[i] += [average_bin_size]
            # print average_times[i], average_bin_size - actual_bin_size
    # print len(average_bin[0]), len(average_bin[1])

    hist_bins = np.arange(19.6, 19.82, 0.005)
    print hist_bins

    mu, sigma = norm.fit(average_bin[0])
    print mu, sigma
    # plt.subplot(gs[0])
    plt.hist(average_bin[0], bins=hist_bins, density=True, color='r', label="Bin size histogram, $\mu=%.4f$, $\sigma=%.4f$, Calibration times = 1"%(mu,sigma))
    plt.vlines(actual_bin_size, 0, 140, colors='g', linewidth= 0.8, linestyles='-.', label='actual bin size = %.4f'%actual_bin_size)
    plt.xlabel("Calibration Bin Size", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)
    plt.ylim(0, 180)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=6, edgecolor='green')
    plt.savefig("Calibration_Bin_Size_histogram_1.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

    mu, sigma = norm.fit(average_bin[1])
    print mu, sigma
    # plt.subplot(gs[1])
    plt.hist(average_bin[1], bins=hist_bins, density=True, color='r', label="Bin size histogram, $\mu=%.4f$, $\sigma=%.4f$, Calibration times = 10"%(mu,sigma))
    plt.vlines(actual_bin_size, 0, 60, colors='g', linewidth= 0.8, linestyles='-.', label='actual bin size = %.4f'%actual_bin_size)
    # plt.title("Calibration Code Histogram", family="Times New Roman", fontsize=12)
    plt.xlabel("Calibration Bin Size", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)
    plt.ylim(0, 80)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=6, edgecolor='green')
    plt.savefig("Calibration_Bin_Size_histogram_10.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

    mu, sigma = norm.fit(average_bin[2])
    print mu, sigma
    # plt.subplot(gs[2])
    plt.hist(average_bin[2], bins=hist_bins, density=True, color='r', label="Bin size histogram, $\mu=%.4f$, $\sigma=%.4f$, Calibration times = 100"%(mu,sigma))
    plt.vlines(actual_bin_size, 0, 80, colors='g', linewidth= 0.8, linestyles='-.', label='actual bin size = %.4f'%actual_bin_size)
    # plt.title("Calibration Code Histogram", family="Times New Roman", fontsize=12)
    plt.xlabel("Calibration Bin Size", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)
    plt.ylim(0, 100)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=6, edgecolor='green')
    plt.savefig("Calibration_Bin_Size_histogram_100.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()

    mu, sigma = norm.fit(average_bin[3])
    print mu, sigma
    # plt.subplot(gs[3])
    plt.hist(average_bin[3], bins=hist_bins, density=True, color='r', label="Bin size histogram, $\mu=%.4f$, $\sigma=%.4f$, Calibration times = 1000"%(mu,sigma))
    plt.vlines(actual_bin_size, 0, 130, colors='g', linewidth= 0.8, linestyles='-.', label='actual bin size = %.4f'%actual_bin_size)
    # plt.title("Calibration Code Histogram", family="Times New Roman", fontsize=12)
    plt.xlabel("Calibration Bin Size", family="Times New Roman", fontsize=10)
    plt.ylabel("Counts", family="Times New Roman", fontsize=10)
    plt.ylim(0, 180)
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=6, edgecolor='green')
    plt.savefig("Calibration_Bin_Size_histogram_1000.png", dpi=fig_dpi, bbox_inches='tight')         # save figure
    plt.clf()
    # plt.subplots_adjust(left=0.08, bottom=0.1, right=0.98, top=0.96, wspace=0.2, hspace=0.22)
    # plt.suptitle("Bin Size Histogram", family="Times New Roman", fontsize=10)


    # time_interval1 = []
    # digital_code1 = []
    # time_range = np.arange(0,200,0.1)
    # for i in xrange(len(time_range)):
    #     digital_code1 += [time_to_digital(time_range[i], Tfr_Delay_Cell, Trf_Delay_Cell)]
    # time_interval1 = time_range
    # time_interval, digital_code = Ideal_Transfer_Function(average_bin_size)
    #
    # plt.plot(time_interval1, digital_code1, color='b',marker='X', linewidth=0.2, markersize=0.02, label='Actual Transfer Function')
    # plt.plot(time_interval, digital_code, color='r',marker='X', linewidth=0.2, markersize=0.02, label='Ideal Transfer Function')
    # plt.title("TDC INL Estimate", family="Times New Roman", fontsize=12)
    # plt.xlabel("Time interval [ps]", family="Times New Roman", fontsize=10)
    # plt.ylabel("Digital code", family="Times New Roman", fontsize=10)
    # plt.xticks(family="Times New Roman", fontsize=8)
    # plt.yticks(family="Times New Roman", fontsize=8)
    # plt.legend(fontsize=8, edgecolor='green')
    # plt.grid(linestyle='-.', linewidth=lw_grid)
    # plt.savefig("TDC_Transfer.pdf", dpi=fig_dpi)
    # plt.clf()
    #
    # TDC_INL_Calculate(average_bin_size, Tfr_Delay_Cell, Trf_Delay_Cell)
    # TDC_DNL_Calculate(average_bin_size, Tfr_Delay_Cell, Trf_Delay_Cell)
    # print "Ok!"
#=============================================================================#
if __name__ == "__main__":
    main()
