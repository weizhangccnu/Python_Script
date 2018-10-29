import sys
import csv
import json
import os, os.path
# import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile
from collections import OrderedDict
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data
#======================================================================#
def read_excel():
    rd_data = get_data("LOCx2 Passed Chips in Trays.xlsx")
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
    print len(sheet_data)
    print sheet_data
    print sheet_data[0][0]

    for i in xrange(len1):
        for j in xrange(len2):
            for k in xrange(len3):
                print i, j, k
                sheet_data[i][j*2][k] =  rd_data[rd_data.keys()[i]][j][k]
                # print rd_data[rd_data.keys()[i]][j][k]
                sheet_data[i][j*2+1][k] = search_file(rd_data[rd_data.keys()[i]][j][k])
        sv_data.update({rd_data.keys()[i]: sheet_data[i]})
    save_data("LOCx2 Passed Chips in Trays_Runpassed.xlsx", sv_data)
    # print rd_data.values()[0][1]

#======================================================================#
def main():
    excel_filename = ['LOCx2_13_14_15.xlsx']
    read_excel()
    # for i in xrange(3):
    #     search_file(123)
    print "Ok"
#======================================================================#
## search file
def search_file(chip_id):
    Check_err = 0
    File_exist = 0
    path = "BER setup2"
    filenum = 0
    for filename in os.listdir(path):
        if filename.find("%s"%chip_id) != -1:                 # find Chip_ID == filename
            filenum += 1
            File_exist = 1
            fp = os.path.join(path, filename)                 # find filepath
            with open(fp, 'r') as chip_id_file:
                for line in chip_id_file.readlines():
                    if len(line.split()) == 1:
                        if line.split()[0] == 'Pass':
                            Check_err = 1

    if Check_err == 1 and File_exist == 1:
        return "P"
    elif Check_err == 0 and File_exist == 1:
        return "NP"
    elif File_exist == 0:
        return "NF"
    else:
        return "MF"
#======================================================================#
if __name__ == "__main__":
  main()
