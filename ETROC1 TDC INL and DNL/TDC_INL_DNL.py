import os
import sys
import time
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
'''
This python script is used to estimate ETROC0 TDC INL and DNL
@author: Wei Zhang
@date: May 5, 2019
@address: SMU dallas, TX
'''
#======================================================================#
## plot parameters
hist_bins = 30                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#=============================================================================#
## measure time interval via TDC
# @param[in] time_interval: time interval
# @param[in] Tfr time of 63 delay cells
# @param[in] Trf time of 63 delay cells
def Measure_Interval(time_interval, Tfr_Delay_Cell, Trf_Delay_Cell):
    # print time_interval
    sum = 0
    digital_code = 0
    for i in xrange(700):
        Delay_Cell_Time = 0
        if sum < time_interval:
            digital_code += 1
            if (i/63)%2 == 0:
                if i%2 == 0:
                    Delay_Cell_Time = Tfr_Delay_Cell[i%63]
                else:
                    Delay_Cell_Time += Trf_Delay_Cell[i%63]
            else:
                if i%2 == 0:
                    Delay_Cell_Time += Tfr_Delay_Cell[i%63]
                else:
                    Delay_Cell_Time += Trf_Delay_Cell[i%63]
            sum += Delay_Cell_Time
            # print i, Delay_Cell_Time, sum
    return digital_code

#=============================================================================#
## Ideal transfer function
def Ideal_Transfer_Function():
    average_bin = 20                                        # average bin size
    time_interval = []
    digital_code = []
    for i in xrange(12500):                                 # TDC range scope from 0 ps to 12.5 ns
        time_interval += [i/1.0]
        digital_code += [((i/1.0)/20)]
        # print i, digital_code
    return time_interval, digital_code

#=============================================================================#
## TDC INL Calculate
def TDC_INL_Calculate():
    pass
#=============================================================================#
## main function
def main():

    # Tfr_mu = 18             # The mu of Tfr is about 18 ps
    # Tfr_sigma = 0.5         # The sigma of Tfr is about 0.5 ps
    #
    # Trf_mu = 21             # The mu of Trf is about 21 ps
    # Trf_sigma = 0.5         # The sigma of Trf is about 0.5 ps
    #
    # # generate 63 delay cell with different Tfr and Trf due to mismatch
    # Tfr_delay_cell = np.random.normal(Tfr_mu, Tfr_sigma, 63)
    # Trf_delay_cell = np.random.normal(Trf_mu, Trf_sigma, 63)
    Tfr_Delay_Cell = [17.67580209, 18.21670517, 18.92140628, 17.34008907, 17.44265303,
    17.81959981, 16.99166971, 18.47667139, 17.41637065, 18.28784679,
    18.05565831, 17.63593543, 18.02388035, 18.10198041, 18.41979584,
    18.0076968,  17.64701811, 18.12378404, 18.73080105, 18.92094868,
    18.54833543, 18.78684639, 17.53028602, 18.74735114, 16.98870835,
    17.79106227, 18.32699514, 18.10865045, 18.46591091, 17.80923658,
    16.9525751,  18.27020017, 18.48407655, 17.97931917, 18.56938946,
    18.99311377, 17.15182244, 18.69289827, 17.38784131, 17.96451595,
    19.00971717, 17.34677605, 17.8233227,  18.12472858, 17.93105869,
    18.11314733, 18.31673184, 17.79027327, 17.42201096, 17.99163869,
    18.52522331, 17.56175264, 17.88688472, 18.37372174, 18.67551556,
    18.68570143, 17.66606446, 18.03884627, 18.74840382, 18.19499854,
    17.92244332, 18.07980731, 17.83499145]
    Trf_Delay_Cell = [20.91007022, 22.44706074, 20.28512074, 21.14421197, 21.64392078,
    20.82871966, 20.92104431, 20.94490652, 21.042155,   21.92561132,
    20.82833285, 21.13681169, 20.86036771, 20.92919224, 21.739083,
    21.17532474, 21.65972149, 20.5719646,  21.77152559, 20.09009963,
    21.2229373,  20.83390884, 20.94396492, 21.07742464, 20.92924945,
    21.013995,   21.08989292, 20.91967974, 21.28056169, 20.91485696,
    20.65922497, 21.17651337, 21.91732342, 21.36400787, 21.58312019,
    21.45023491, 20.98842694, 20.41591534, 20.95443314, 19.59405158,
    20.25648915, 21.22608027, 20.41216676, 20.97518253, 21.37278011,
    20.9552742,  20.81053212, 20.63548905, 19.99083733, 19.99231219,
    20.2314484,  21.11471578, 21.81860545, 20.31381881, 21.29123206,
    20.7565477,  21.41875059, 21.4527391,  20.28273762, 20.38291829,
    20.85283457, 21.5522761,  21.48619254]

    print Tfr_Delay_Cell
    print Trf_Delay_Cell

    time_interval1 = []
    digital_code1 = []
    for i in xrange(12500):
        digital_code1 += [Measure_Interval(i, Tfr_Delay_Cell, Trf_Delay_Cell)]
        time_interval1 += [i]
        # print i, digital_code1
    print time_interval1, digital_code1
    # digital_code1 = Measure_Interval(1225, Tfr_Delay_Cell, Trf_Delay_Cell)
    time_interval, digital_code = Ideal_Transfer_Function()

    plt.plot(time_interval, digital_code, color='r',marker='X', linewidth=0.2, markersize=0.02, label='Ideal Transfer Fucntion')
    plt.plot(time_interval1, digital_code1, color='b',marker='X', linewidth=0.2, markersize=0.02, label='Actual Transfer Fucntion')
    plt.title("TDC INL Estimate", family="Times New Roman", fontsize=12)
    plt.xlabel("Time interval [ps]", family="Times New Roman", fontsize=10)
    plt.ylabel("Digital code", family="Times New Roman", fontsize=10)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.legend(fontsize=8, edgecolor='green')
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.savefig("TDC_INL.pdf", dpi=fig_dpi)
    print "Ok!"
#=============================================================================#
if __name__ == "__main__":
    main()
