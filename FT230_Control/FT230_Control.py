import os
import sys
import copy
import time
import math
import serial
'''
@ Description: The FT230 is a USB to serial UART interface that is as data brige between PC and STM32.
@ author: Wei Zhang
@ date: 2022-09-29
'''
#----------------------------------------------------------------------------------#
def main():
    i = 0
    string1 = ['a', 'b', 'c', 'd', 'e', 'f']
    ser = serial.Serial('COM15', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    if ser.isOpen():
        print("serial port open success!")
    print("Serial port: %s"%ser.name)
    
    while(1):
        # send character "1"
        ser.write(string1[i].encode())  
        time.sleep(1)   
        i = i + 1
        if i == 6:
            i = 0
        print(i, string1[i])                 
    
    print("Ok!")

#----------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()




