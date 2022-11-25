import os
import sys
import copy
import time
import math
import serial
'''
@ Description: using python code controls the CL-200A device
@ author: Wei Zhang
@ date: 2022-09-01
'''
#----------------------------------------------------------------------------------#
def main():
    exp = [10**-4, 10**-3, 10**-2, 10**-1, 10**0, 10**1, 10**2, 10**3, 10**4, 10**5]
    command_link    = "0x02 0x30 0x30 0x35 0x34 0x31 0x20 0x20 0x20 0x03 0x31 0x33 0x0d 0x0a"
    command_hold    = "0x02 0x39 0x39 0x35 0x35 0x31 0x20 0x20 0x30 0x03 0x30 0x32 0x0d 0x0a"
    command_setEXT  = "0x02 0x30 0x30 0x34 0x30 0x31 0x30 0x20 0x20 0x03 0x30 0x36 0x0d 0x0a"
    command_measure = "0x02 0x39 0x39 0x34 0x30 0x32 0x31 0x20 0x20 0x03 0x30 0x34 0x0d 0x0a"

    command_EvXY    = "0x02 0x30 0x30 0x30 0x32 0x31 0x33 0x30 0x30 0x03 0x30 0x33 0x0d 0x0a"

    command_EvTcp   = "0x02 0x30 0x30 0x30 0x38 0x31 0x33 0x30 0x30 0x03 0x30 0x39 0x0d 0x0a"

    str_command_link     = ''.join([chr(int(i, 16)) for i in command_link.split()])
    str_command_hold     = ''.join([chr(int(i, 16)) for i in command_hold.split()])
    str_command_setEXT   = ''.join([chr(int(i, 16)) for i in command_setEXT.split()])
    str_command_measure  = ''.join([chr(int(i, 16)) for i in command_measure.split()])
    str_command_EvXY     = ''.join([chr(int(i, 16)) for i in command_EvXY.split()])
    str_command_EvTcp     = ''.join([chr(int(i, 16)) for i in command_EvTcp.split()])

    ser = serial.Serial('COM9', baudrate=9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)
    if ser.isOpen():
        print("serial port open success!")
    print("Serial port: %s"%ser.name)

    ser.write(str_command_link.encode())                      # link CLA200A device
    time.sleep(1)
    print("%s"%ser.readline())
    
    time.sleep(1)
    ser.write(str_command_hold.encode())                    # hold command 
    
    time.sleep(1)
    ser.write(str_command_setEXT.encode())                  # EXT command
    time.sleep(1)
    print("%s"%ser.readline())

    time.sleep(1)
    ser.write(str_command_measure.encode())                 # measure command 

    # time.sleep(1)
    # ser.write(str_command_EvXY.encode())                    # measure EvXY value
    # time.sleep(1)

    # EvXY_str = ser.readline()                               # read back EvXY value

    # print(EvXY_str)
    # print(EvXY_str.decode().split('+')[1], EvXY_str.decode().split('+')[2], EvXY_str.decode().split('+')[3][:-4])

    # EV_value = int(EvXY_str.decode().split('+')[1][:-1]) * exp[int(EvXY_str.decode().split('+')[1][-1])]
    # X_value = int(EvXY_str.decode().split('+')[2][:-1]) * exp[int(EvXY_str.decode().split('+')[2][-1])]
    # Y_value = int(EvXY_str.decode().split('+')[3][:-4][:-2]) * exp[int(EvXY_str.decode().split('+')[3][:-4][-2])]

    # print("EV value: %f"%EV_value)
    # print("X value: %f"%X_value)
    # print("Y value: %f"%Y_value)


    time.sleep(1)
    ser.write(str_command_EvTcp.encode())                    # measure EvXY value
    time.sleep(1)

    EvTcp_str = ser.readline()                               # read back EvXY value

    print(EvTcp_str)

    EV_value = int(EvTcp_str.decode().split('+')[1][:-1]) * exp[int(EvTcp_str.decode().split('+')[1][-1])]
    Tcp_value = int(EvTcp_str.decode().split('+')[2][:-1]) * exp[int(EvTcp_str.decode().split('+')[2][-1])]
    Delta_uv_value = int(EvTcp_str.decode().split('+')[3][:-4][:-2]) * exp[int(EvTcp_str.decode().split('+')[3][:-4][-2])]

    print("EV value: %f"%EV_value)
    print("Tcp value: %f"%Tcp_value)
    print("Delta uv value: %f"%Delta_uv_value)

    print("Ok!")

#----------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()




