#!/usr/bin/env python3

import socket
import sys
from time import sleep
import random
from struct import pack
import serial

#get magneto reading from arduino
#ls /dev/tty* before and after connecting the sensor to determine the serial port
ser = serial.Serial("/dev/ttyACM1", 9600) #arduino uses 9600 baud

#TODO previous N axis readings
prv = list() # list of previous x,y,z axis reading
window_size = 10

isFirst = True
bay = 1 #bayid of bay 1


def get_window():
    """
    returns a list of window of [window_size] readings
    """
    print("getting list of windows")
    window = list()
    for i in range(window_size):
        #decodes each line sent on serial port
        #from byte to utf-8 string
        #count = ser.readline()
        Xout = ser.readline().decode("utf-8")
        Yout = ser.readline().decode("utf-8")
        Zout = ser.readline().decode("utf-8")
        window.append([float(Xout.strip("\r\n")),
                       float(Yout.strip("\r\n")),
                       float(Zout.strip("\r\n")) ])

    #TODO somehow account for noise in readings

    return window


while 1:
    #no adjustment for magnetic declination on the arduino
    #first run saves readings as previous reading without sending anything
    if isFirst:
        first_window = get_window() #RUN TWICE to let readings settle
        first_window = get_window()
        prv = first_window[9] #takes last reading
        #can be changed to avg(first_window[,0]) to take avg of all x readings in the window
        isFirst = not isFirst

    ################################
    #determine bay vacancy status
    ################################
    window = get_window()
    ndp = 1 #number of decimal pts to round
    xchanged = (round(prv[0], ndp) - round(window[9][0], ndp) ) != 0 #maybe keep 2 or 3 decimals???
    ychanged = (round(prv[1], ndp) - round(window[9][1], ndp) ) != 0 #maybe keep 2 or 3 decimals???
    zchanged = (round(prv[2], ndp) - round(window[9][2], ndp) ) != 0 #maybe keep 2 or 3 decimals???
    print("x: {} \t y: {} \t z: {}".format(round(window[9][0], ndp), round(window[9][1], ndp), round(window[9][2], ndp)))

    bvs = 1 #assume bay is vacant: 1; occupied: 0

    #"calculate" the vacancy based on window
    if xchanged or ychanged or zchanged:
        print("bay status changed")
        #send bay vacancy status changed
        bvs = not bvs

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '172.20.10.3', 65000 #static ip address of server
    server_address = (host, port)

    #Pack three 32-bit floats into message and send
    message = pack('5f', bay, bvs, window[9][0] , window[9][1], window[9][2])
    sock.sendto(message, server_address)

    #update previous readings with last reading
    prv = window[9]


    sleep(1) #1sec

