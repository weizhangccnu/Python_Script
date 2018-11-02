import sys
import csv
import json
import time
import os, os.path
from collections import OrderedDict
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data
'''
LOCx2 chips BER Check and EYE Check, This is a very interesting project for me.
DT is coming. AI is very important for our life.
@author: Wei Zhang
@date: Nov 1, 2018
@address: SMU dallas TX
'''
#======================================================================#
## BER check for checking each chip pass or fail
def BER_Check():
    with open("BER_Record.txt", 'w') as recordfile:
        rd_data = get_data("LOCx2 Passed Chips in Trays_20181101.xlsx")
        print rd_data.keys()                                                       # print keys
        sv_data = OrderedDict()                                                    # Excel save directory
        print rd_data[rd_data.keys()[0]]
        print rd_data[rd_data.keys()[1]]
        print rd_data[rd_data.keys()[2]]
        len1 = len(rd_data)
        len2 = len(rd_data.values()[0])
        len3 = len(rd_data.values()[0][0])
        print len1, len2, len3
        sheet_data = [[[0 for y in xrange(len3)] for x in xrange(len2*2)] for z in xrange(len1)]                # create a sheet list for Excel
        All_Chipid = []                                                                                         # restore All Chip ID
        for i in xrange(len1):
            for j in xrange(len2):
                for k in xrange(len3):
                    print i, j, k
                    sheet_data[i][j*2][k] =  rd_data[rd_data.keys()[i]][j][k]
                    sheet_data[i][j*2+1][k] = search_ber_file(rd_data[rd_data.keys()[i]][j][k])
                    All_Chipid += [rd_data[rd_data.keys()[i]][j][k]]
                    if search_ber_file(rd_data[rd_data.keys()[i]][j][k]) != "P" and search_ber_file(rd_data[rd_data.keys()[i]][j][k]) != "MP" and  rd_data[rd_data.keys()[i]][j][k] != 9008:    # list NP, NF chip location
                        recordfile.write("%s %2d %2d %s %s\n"%(rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k], search_ber_file(rd_data[rd_data.keys()[i]][j][k])))
            sv_data.update({rd_data.keys()[i]: sheet_data[i]})                              # sheet_name and sheet_data
        save_data("LOCx2 Passed Chips in Trays_20181101_BERChecked.xlsx", sv_data)          # save excel file
        # print All_Chipid                                                                  # check unique chip_id
        Repe_Chipid = [val for val in list(set(All_Chipid)) if All_Chipid.count(val) >= 2]  # search repeated  chip_id
        print "Repeted Chip ID:", Repe_Chipid                                               # print repeated chip ID
        with open("Uniqueness.txt", 'w') as uniquenessfile:                                 # save repeated chip ID to txt file
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
    rd_data = get_data("LOCx2 Passed Chips in Trays_20181101.xlsx")
    print rd_data.keys()                                                       #print keys
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
                    if search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) == "MEP" or search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) == "EP":         # use space replace "MEP" and "EP"
                        sheet_data[i][j*2+1][k] = " "
                    else:
                        sheet_data[i][j*2+1][k] = search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record)
                    if search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) != "EP" and search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record) != "MEP" and rd_data[rd_data.keys()[i]][j][k] != 9008:    # list NR, EF, MEP, MEF chip location
                        # print rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k], search_eye_file(rd_data[rd_data.keys()[i]][j][k])
                        eyerecordfile.write("%s %2d %2d %4d %s\n"%(rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k], search_eye_file(rd_data[rd_data.keys()[i]][j][k], eye_record)))
            sv_data.update({rd_data.keys()[i]: sheet_data[i]})                          # sheet_name and sheet_data
    save_data("LOCx2 Passed Chips in Trays_20181101_EYEChecked.xlsx", sv_data)          # save excel file
#======================================================================#
## search file in directory
def search_ber_file(chip_id):
    Check_pass = 0
    path = "BER2"
    filenum = 0
    multifilepath = []
    for filename in os.listdir(path):
        if filename.find("%s"%chip_id) != -1:                     # find Chip_ID == filename
            if filename.split('_')[1].split('p')[1] == "%s"%chip_id:
                filenum += 1
                fp = os.path.join(path, filename)                 # find filepath
                # print os.path.getmtime(fp)
                multifilepath += [fp]
                with open(fp, 'r') as chip_id_file:
                    for line in chip_id_file.readlines():
                        if len(line.split()) == 1:
                            if line.split()[0] == 'Pass':
                                Check_pass = 1
    # if filenum >= 2:
    #     print filenum
    # print filetime
    if Check_pass == 1 and filenum == 1:                        # one file and pass
        return "P"
    elif Check_pass == 0 and filenum == 1:                      # one file and fail
        return "NP"
    elif filenum == 0 :                                         # no such file
        return "NF"
    else:                                                       # multifile check
        multifilepath.sort(key=lambda fn: os.path.getmtime(fn)) # sort by file modified time
        # print multifilepath[-1]
        fp1 = multifilepath[-1]                                 # achieve last modified file
        Check_pass = 0                                          # reset Check_pass variable
        with open(fp1, 'r') as chip_id_file:
            for line in chip_id_file.readlines():               # find Checkpass or not
                if len(line.split()) == 1:
                    if line.split()[0] == 'Pass':
                        Check_pass = 1
        if Check_pass == 1:
            return "MP"                                         # Multifile check pass
        else:
            return "MF"                                         # Multifile check fail
#======================================================================#
## search_eye_file in eye1 or eye2 directory
def search_eye_file(chip_id, eye_record):
    eye_results = [eye_record[row] for row in xrange(len(eye_record)) if int(eye_record[row][0]) == chip_id]
    # print eye_results
    # print len(eye_results)
    if len(eye_results) == 0:                                   # no records
        return "NR"
    elif len(eye_results) == 1:                                 # only one records
        if eye_results[len(eye_results)-1][1] == '1':
            return "EP"
        else:
            return "EF"
    else:                                                       # more than one record
        if eye_results[len(eye_results)-1][1] == '1':
            return "MEP"                                        # multi-record Eye Pass
        else:
            return "MEF"                                        # multi-record Eye Fail
#======================================================================#
## main function
def main():
    BER_Check()                                                 # Execute main function
    # EYE_Check()                                                 # execute Eyediagram check
    # print search_eye_file(6666)                               # test search_eye_file function
    # print search_ber_file(1599)                                # test search_ber_file function
    print "Ok"                                                  # execute over
#======================================================================#
## if statement
if __name__ == "__main__":
  main()
