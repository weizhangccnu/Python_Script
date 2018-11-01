import sys
import csv
import json
import os, os.path
from collections import OrderedDict
from pyexcel_xlsx import get_data
from pyexcel_xlsx import save_data
#======================================================================#
## BER check for checking each chip pass or fail
def BER_Check():
    with open("BER_Record.dat", 'w') as recordfile:
        rd_data = get_data("LOCx2 Passed Chips in Trays_20181031.xlsx")
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
        All_Chipid = []
        for i in xrange(len1):
            for j in xrange(len2):
                for k in xrange(len3):
                    print i, j, k
                    sheet_data[i][j*2][k] =  rd_data[rd_data.keys()[i]][j][k]
                    sheet_data[i][j*2+1][k] = search_ber_file(rd_data[rd_data.keys()[i]][j][k])
                    All_Chipid += [rd_data[rd_data.keys()[i]][j][k]]
                    if search_ber_file(rd_data[rd_data.keys()[i]][j][k]) != "P":    # list NP, NF chip location
                        recordfile.write("%s %2d %2d %s %s\n"%(rd_data.keys()[i], j, k, search_ber_file(rd_data[rd_data.keys()[i]][j][k]), rd_data[rd_data.keys()[i]][j][k]))
            sv_data.update({rd_data.keys()[i]: sheet_data[i]})                  # sheet_name and sheet_data
        save_data("LOCx2 Passed Chips in Trays_V1_BERChecked_20181031.xlsx", sv_data)        # save excel file
        print All_Chipid                                                            # check unique chip_id
        Repe_Chipid = [val for val in list(set(All_Chipid)) if All_Chipid.count(val) >= 2]      # search repeated  chip_id
        print Repe_Chipid
        with open("Uniqueness.dat", 'w') as uniquenessfile:
            for i in xrange(len1):
                for j in xrange(len2):
                    for k in xrange(len3):
                        # print i, j, k
                        for id in xrange(len(Repe_Chipid)):
                            if Repe_Chipid[id] == rd_data[rd_data.keys()[i]][j][k]:
                                print rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k]
                                uniquenessfile.write("%s %2d %2d %s\n"%(rd_data.keys()[i], j, k, rd_data[rd_data.keys()[i]][j][k]))
#======================================================================#
## Eyediagram check
def EYE_Check():
    with open("EYE_Record.dat", 'w') as recordfile:
        rd_data = get_data("LOCx2 Passed Chips in Trays_V1.xlsx")
        print rd_data.keys()                                                       #print keys
        sv_data = OrderedDict()
        print rd_data[rd_data.keys()[0]]
        print rd_data[rd_data.keys()[1]]
        print rd_data[rd_data.keys()[2]]
        len1 = len(rd_data)
        len2 = len(rd_data.values()[0])
        len3 = len(rd_data.values()[0][0])
        print len1, len2, len3
        sheet_data = [[[0 for y in xrange(len3)] for x in xrange(len2)] for z in xrange(len1)]
        for i in xrange(len1):
            for j in xrange(len2):
                for k in xrange(len3):
                    print i, j, k
                    sheet_data[i][j][k] =  rd_data[rd_data.keys()[i]][j][k]
                    # sheet_data[i][j*2+1][k] = search_file(rd_data[rd_data.keys()[i]][j][k])
                    # if search_file(rd_data[rd_data.keys()[i]][j][k]) != "P":    # list NP, NF chip location
                        # recordfile.write("%s %2d %2d %s\n"%(rd_data.keys()[i], j, k, search_file(rd_data[rd_data.keys()[i]][j][k])))
            sv_data.update({rd_data.keys()[i]: sheet_data[i]})                  # sheet_name and sheet_data
        save_data("LOCx2 Passed Chips in Trays_V1_EYEChecked.xlsx", sv_data)        # save excel file
#======================================================================#
## search file in directory
def search_ber_file(chip_id):
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
## search_eye_file in eye1 or eye2 directory
def search_eye_file(chip_id):
    filename = "LOCx2_QA_spring2018_Eye1_Eye2.txt"
    i = 0
    Chip_id_Dict = {}
    name_row = 0
    value_row = 0
    with open(filename, 'r') as eyefile:
        for line in eyefile.readlines():
            i += 1
            j = 0
            flag = 0
            if len(line.split()) == 34 :
                name_row = i
                name = line.split()[0]                   # achieve chip id
            elif len(line.split()) == 29:
                flag = 1
                value_row = i
                value = line.split()[27]
            if value_row - name_row >= 2 and flag == 1 and name >= 10:
                print name_row, name, value
#======================================================================#
## main function
def main():
    # BER_Check()                         # Execute main function
    # EYE_Check()                         # execute Eyediagram check
    search_eye_file(4107)
    print "Ok"                          # execute ended
#======================================================================#
## if statement
if __name__ == "__main__":
  main()
