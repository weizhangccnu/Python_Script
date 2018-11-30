import sys
import csv
import json
import time
import os, os.path
from collections import OrderedDict
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.optimize import curve_fit
from scipy.stats import norm
'''
LOCx2 chips BER Check and EYE Check, This is a very interesting project for me.
DT is coming. AI is very important for our life in future.
@author: Wei Zhang
@date: Nov 1, 2018
@address: SMU Dallas, TX
'''
Excel_filename = "LOCx2 Passed Chips in Trays_20181109.xlsx"

#======================================================================#
## plot parameters
hist_bins = 40                  # histogram bin counts
lw_grid = 0.5                   # grid linewidth
fig_dpi = 800                   # save figure's resolution
#======================================================================#
## BER check for checking each chip pass or fail
def BER_Check():
    with open("BER_Record_20181109.txt", 'w') as recordfile:
        rd_data = get_data(Excel_filename)
        print rd_data.keys()                                                                                    # print keys
        sv_data = OrderedDict()                                                                                 # Excel save directory
        print rd_data[rd_data.keys()[0]]
        print rd_data[rd_data.keys()[1]]
        print rd_data[rd_data.keys()[2]]
        len1 = len(rd_data)
        len2 = len(rd_data.values()[0])
        len3 = len(rd_data.values()[0][0])
        print len1, len2, len3
        sheet_data = [[[0 for y in xrange(len3)] for x in xrange(len2*2)] for z in xrange(len1)]                # create a sheet list for Excel
        for i in xrange(len1):
            for j in xrange(len2):
                for k in xrange(len3):
                    print i, j, k
                    sheet_data[i][j*2][k] =  rd_data[rd_data.keys()[i]][j][k]                                   # Chip ID
                    sheet_data[i][j*2+1][k] = search_ber_file(rd_data[rd_data.keys()[i]][j][k])                 # BER Check Results
                    if search_ber_file(rd_data[rd_data.keys()[i]][j][k]) != "BP" and search_ber_file(rd_data[rd_data.keys()[i]][j][k]) != "BMP" and  rd_data[rd_data.keys()[i]][j][k] != 9008:    # list NP, NF chip location
                        recordfile.write("%s %2d %2d %s %s\n"%(rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k], search_ber_file(rd_data[rd_data.keys()[i]][j][k])))
            sv_data.update({rd_data.keys()[i]: sheet_data[i]})                                                  # sheet_name and sheet_data
        save_data("LOCx2 Passed Chips in Trays_20181109_BERChecked.xlsx", sv_data)                              # save excel file
#======================================================================#
## Unique Check
def Unique_Check():
    rd_data = get_data(Excel_filename)
    sv_data = OrderedDict()
    len1 = len(rd_data)
    len2 = len(rd_data.values()[0])
    len3 = len(rd_data.values()[0][0])                                                          # Excel save directory
    sheet_data = [[[0 for y in xrange(len3)] for x in xrange(len2*2)] for z in xrange(len1)]    # create a sheet list for Excel
    All_Chipid = []                                                                             # restore All Chip ID
    for i in xrange(len1):
        for j in xrange(len2):
            for k in xrange(len3):
                print i, j, k
                All_Chipid += [rd_data[rd_data.keys()[i]][j][k]]
        # print All_Chipid                                                                      # check unique chip_id
    Repe_Chipid = [val for val in list(set(All_Chipid)) if All_Chipid.count(val) >= 2]          # search repeated  chip_id
    print "Repeted Chip ID:", Repe_Chipid                                                       # print repeated chip ID
    with open("Uniqueness.txt", 'w') as uniquenessfile:                                         # save repeated chip ID to txt file
        for i in xrange(len1):
            for j in xrange(len2):
                for k in xrange(len3):
                    # print i, j, k
                    for id in xrange(len(Repe_Chipid)):
                        if Repe_Chipid[id] == rd_data[rd_data.keys()[i]][j][k] and Repe_Chipid[id] != 9008:
                            print rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k]
                            uniquenessfile.write("%s %2d %2d %s\n"%(rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k]))
#======================================================================#
## Eyediagram check
def EYE_Check():
    filename = "LOCx2_QA_spring2018_Eye1_Eye2.txt"          # eye test results record file
    i = 0                                                   # record row number
    name_row = 0                                            # chip id row number
    value_row = 0                                           # pass row number
    eye_record = []                                         # eye record list
    with open(filename, 'r') as eyefile:                    # read eye1 and eye.txt file
        for line in eyefile.readlines():
            i += 1
            flag = 0
            if len(line.split()) == 34 :
                name_row = i
                name = line.split()[0]                      # achieve chip id
            elif len(line.split()) == 29:
                flag = 1
                value_row = i
                value = line.split()[27]
            if value_row - name_row >= 2 and flag == 1 and name >= 10:
                # print name_row, name, value
                eye_record += [[name, value]]
    rd_data = get_data(Excel_filename)
    print rd_data.keys()                                    #print keys
    sv_data = OrderedDict()
    print rd_data[rd_data.keys()[0]]
    print rd_data[rd_data.keys()[1]]
    print rd_data[rd_data.keys()[2]]
    len1 = len(rd_data)
    len2 = len(rd_data.values()[0])
    len3 = len(rd_data.values()[0][0])
    print len1, len2, len3
    sheet_data = [[[0 for y in xrange(len3)] for x in xrange(len2*2)] for z in xrange(len1)]
    i = j = k = 0
    with open("EYE_Record.txt", 'w') as eyerecordfile:
        for i in xrange(len1):
            for j in xrange(len2):
                for k in xrange(len3):
                    print i, j, k                                                                           # print sheet number, row number, and column number
                    sheet_data[i][j*2][k] =  rd_data[rd_data.keys()[i]][j][k]
                    if search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) == "EMP" or search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) == "EP":         # use space replace "MEP" and "EP"
                        sheet_data[i][j*2+1][k] = " "
                    else:
                        sheet_data[i][j*2+1][k] = search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record)
                    if search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) != "EP" and search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) != "EMP" and rd_data[rd_data.keys()[i]][j][k] != 9008:    # list NR, EF, MEP, MEF chip location
                        # print rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k], search_eye_file(rd_data[rd_data.keys()[i]][j][k])
                        eyerecordfile.write("%s %2d %2d %4d %s\n"%(rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k], search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record)))
            sv_data.update({rd_data.keys()[i]: sheet_data[i]})                          # sheet_name and sheet_data
    save_data("LOCx2 Passed Chips in Trays_20181109_EYEChecked.xlsx", sv_data)          # save excel file
#======================================================================#
## search file in directory
def search_ber_file(chip_id):
    Check_pass = 0
    Check_fail = 0
    path = "BER2"
    filenum = 0
    multifilepath = []
    for filename in os.listdir(path):
        if filename.find("%s"%chip_id) != -1:                       # find Chip_ID == filename
            if filename.split('_')[1].split('p')[1] == "%s"%chip_id:
                filenum += 1
                fp = os.path.join(path, filename)                   # find filepath
                # print os.path.getmtime(fp)
                multifilepath += [fp]
                # print multifilepath
                with open(fp, 'r') as chip_id_file:
                    for line in chip_id_file.readlines():
                        if len(line.split()) == 1:
                            if line.split()[0] == 'Pass':
                                Check_pass = 1
                            elif line.split()[0] == 'Fail':
                                Check_fail = 1
    # print multifilepath
    # print Check_pass
    # print Check_fail
    if Check_pass == 1 and filenum == 1:                            # one file and pass
        return "BP"
    elif Check_fail == 1 and filenum == 1:
        return "BF"
    elif Check_pass == 0 and Check_fail == 0 and filenum == 1:                          # one file and fail
        Re_BF_Check = search_single_file(fp)                        # check single file due to this file is no Pass and ending line
        if Re_BF_Check == 1:
            return "BP"
        else:
            return "BF"
    elif filenum == 0 :                                             # no such file
        return "BNR"
    else:                                                           # multifile check
        multifilepath.sort(key=lambda fn: os.path.getmtime(fn))     # sort by file modified time
        # print multifilepath[-1]
        fp1 = multifilepath[-1]                                     # achieve last modified file
        Check_pass = 0                                              # reset Check_pass variable
        with open(fp1, 'r') as chip_id_file:
            for line in chip_id_file.readlines():                   # find Checkpass or not
                if len(line.split()) == 1:
                    if line.split()[0] == 'Pass':
                        Check_pass = 1

        if Check_pass == 1:
            return "BMP"                                            # Multifile check pass
        else:
            Re_BMP_Check = search_single_file(fp1)
            if Re_BMP_Check == 1:
                return "BMP"                                        # Multifile check fail
            else:
                return "BMF"                                        # Multifile check fail

#======================================================================#
## search single file
def search_single_file(filepath):
    # print filepath
    counts = len(open(filepath, 'r').readlines())
    cnt = 0
    # print counts / 657
    # print counts % 657
    if counts / 657 == 1 and counts % 657 == 0:                     # 657 lines
        cnt = 0
    elif counts / 657 == 1 and counts % 657 == 2:                   # 659 lines
        cnt = 1
    elif counts / 657 == 1 and counts % 657 >= 4 and counts % 657 <= 50:               # 660 lines
        cnt = 2
    else:
        cnt = 3
    # print "cnt: %d"%cnt
    with open(filepath, 'r') as singlefile:
        LineNum = [43, 64, 95, 116, 147, 168, 254, 275, 306, 327, 358, 379]
        LineNum1 = [45, 66, 97, 118, 149, 170, 256, 277, 308, 329, 360, 381]
        LineRes = []
        i = 0                                                       # record row number
        for line in singlefile.readlines():
            i += 1
            if cnt == 0 or cnt == 2:                                # 657 lines
                if i in LineNum:
                    LineRes += [line.split()[0]]
            elif cnt == 1:                                          # 659 lines
                if i in LineNum1:
                    LineRes += [line.split()[0]]
            else:
                LineRes = [0 for i in xrange(12)]
        # print LineRes
        if LineRes[0] == '0' and LineRes[1] == '0' and LineRes[2] == '0' and LineRes[3] == '0' and LineRes[4] == '0' and LineRes[5] == '0' or LineRes[6] == '1' or LineRes[7] == '1' or LineRes[8] == '1' or LineRes[9] == '1' or LineRes[10] == '1' or LineRes[11] == '1':
            return 1
        else:
            return 0
#======================================================================#
## search_eye_file in eye1 or eye2 directory
def search_eye_file(chip_id, eye_record):
    # print eye_record
    # print type(eye_record[0][0])
    # print type(int(eye_record[0][0]))
    # print type(int(chip_id))
    eye_results = [eye_record[row] for row in xrange(len(eye_record)) if eye_record[row][0] == "%s"%chip_id]
    # print eye_results
    if len(eye_results) == 0:                                   # no records
        return "ENR"
    elif len(eye_results) == 1:                                 # only one records
        if eye_results[len(eye_results)-1][1] == '1':
            return "EP"
        else:
            return "EF"
    else:                                                       # more than one record
        if eye_results[len(eye_results)-1][1] == '1':
            return "EMP"                                        # multi-record Eye Pass
        else:
            return "EMF"                                        # multi-record Eye Fail
#======================================================================#
## research_ber_check
def repeated_ber_check():
    Excel_filename = "Sinewave_BER1_Results.xlsx"               # Excel filename
    rd_data = get_data(Excel_filename)
    with open("BER_Record_20181109.txt", 'r') as ber_record_file, open("Repeat_BER_Check.txt", 'w') as reber_file:      # BER Record file
        for row in ber_record_file.readlines():
            chip_id = row.split()[3]                            # achieve chip id
            Chip_Test = 0
            Chip_Test1 = 0
            Chip_Result = 0
            result = "BNR"
            for row in xrange(4, len(rd_data[rd_data.keys()[1]]), 1):
                if rd_data[rd_data.keys()[1]][row][0] == int(chip_id):
                    Chip_Test = 1                                       # Chip test
                # print len(rd_data[rd_data.keys()[1]][row])
                if len(rd_data[rd_data.keys()[1]][row]) >= 25:
                    if rd_data[rd_data.keys()[1]][row][0] == int(chip_id):
                        # print rd_data[rd_data.keys()[1]][row]
                        Chip_Test1 = 1
                        Chip_Result = rd_data[rd_data.keys()[1]][row][24]
            if Chip_Test == 1 and Chip_Test1 == 0:
                result = "BFNT"
            elif Chip_Test1 == 1 and Chip_Result == 1:
                result = "BP"
            elif Chip_Test == 0 and Chip_Test1 == 0:
                result = "BNR"
            else:
                result = "BF"
            print chip_id, result
            reber_file.write("%s %s\n"%(chip_id, result))
#======================================================================#
## current statistics
def current_statistics():
    filename = "LOCx2_QA_spring2018_Eye1_Eye2.txt"          # eye test results record file
    i = 0                                                   # record row number
    name_row = 0                                            # chip id row number
    value_row = 0                                           # pass row number
    eye_record = []                                         # eye record list
    chipid_row = 0
    chip_current = []                                       # chip current record
    current_statistics = []
    with open(filename, 'r') as eyefile:                    # read eye1 and eye.txt file
        for line in eyefile.readlines():
            i += 1
            flag = 0
            if len(line.split()) == 34:
                chipid_row = i
                chipid = line.split()[0]
            elif len(line.split()) != 34:
                flag = 1
                value_row = i
            if value_row - chipid_row >= 1 and flag == 1 and (line.split()[0] == '40' or line.split()[0] == '40.0') and line.split()[1] == '1':
                # print i,  chipid_row, chipid, line.split()[0],  line.split()[1], type(line.split()[2])
                chip_current += [[chipid, line.split()[2]]]
        # print chip_current
    with open("over_three_sigma.txt", 'w') as outfile:
        rd_data = get_data(Excel_filename)
        len1 = len(rd_data)
        len2 = len(rd_data.values()[0])
        len3 = len(rd_data.values()[0][0])                                                          # Excel save directory
        sheet_data = [[[0 for y in xrange(len3)] for x in xrange(len2*2)] for z in xrange(len1)]    # create a sheet list for Excel
        for i in xrange(len1):
            for j in xrange(len2):
                for k in xrange(len3):
                    if rd_data[rd_data.keys()[i]][j][k] != 9008:
                        # print rd_data.keys()[i], j+1, k+1, rd_data[rd_data.keys()[i]][j][k], [val[1] for val in chip_current if val[0] == '%s'%rd_data[rd_data.keys()[i]][j][k]][-1]
                        singlechip_current = float([val[1] for val in chip_current if val[0] == '%s'%rd_data[rd_data.keys()[i]][j][k]][-1])
                        current_statistics += [singlechip_current]
                        if singlechip_current < 299.99 or singlechip_current > 363.17:
                            outfile.write("%s %2d %2d %4d %s\n"%(rd_data.keys()[i], j+1, k+1, rd_data[rd_data.keys()[i]][j][k], singlechip_current))

    # return current_statistics
    return current_statistics
#======================================================================#
## plot current statistics
def plot_current_statistic(data):
    # print data
    mu, sigma = norm.fit(data)
    print mu, sigma
    plt.hist(data, bins=50, density=True, color='r', label='Current bin')

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 1000)
    p = norm.pdf(x, mu, sigma)
    # print p
    # print len(data), len(p)
    # x_ticks = np.arange(200, 450)
    plt.plot(x, p, color='b', linewidth=1.2, label='Fit results: ${\mu}$ = %.2f,  ${\sigma}$ = %.2f' % (mu, sigma))
    plt.title("Current Histogram", family="Times New Roman", fontsize=12)
    plt.xlabel("Current [mA]", family="Times New Roman", fontsize=10)
    plt.ylabel("Density", family="Times New Roman", fontsize=10)
    plt.xlim(200, 480)

    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.legend(fontsize=8, edgecolor='green')
    plt.savefig("Current_histogram.png", dpi=fig_dpi, bbox_inches='tight')
    plt.clf()
#======================================================================#
## main function
def main():
    # Unique_Check()                                              # Unique check
    # BER_Check()                                                 # Execute main function
    # EYE_Check()                                                 # execute Eyediagram check
    # print search_eye_file(3143)                                 # test search_eye_file function
    # print search_ber_file(5768)                                 # test search_ber_file function
    # repeated_ber_check()                                        # repeated check ber
    data = current_statistics()
    plot_current_statistic(data)
    print "Ok"                                                  # execute over
#======================================================================#
## if statement
if __name__ == "__main__":
  main()
