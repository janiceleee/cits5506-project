#!/usr/bin/env python3

import socket
from time import sleep
from struct import pack
import serial
from statistics import mode

serialPort = "/dev/ttyACM0" #serial port of the arduino
ipAddress = "192.168.1.128" #IP address of server

#get magnetometer readings from arduino
ser = serial.Serial(serialPort, 9600) #arduino uses 9600 baud

prv = list() # list of previous x,y,z axis reading
window_size = 11

isFirst = True
bay = 1 #bayid of bay 1
ndp = 1 #number of decimal places to round

def get_window():
    """
    returns a list of window of [window_size] readings
    """
    print("getting list of windows")
    window = list()
    for i in range(window_size):
        #decodes each line sent on serial port
        #from byte to utf-8 string
        Xout = ser.readline().decode("utf-8").strip("\r\n")
        Yout = ser.readline().decode("utf-8").strip("\r\n")
        Zout = ser.readline().decode("utf-8").strip("\r\n")
        Xout = float(Xout)
        Yout = float(Yout)
        Zout = float(Zout)
        window.append([round(Xout, ndp), round(Yout, ndp), round(Zout, ndp)])

    #Take mode of window_size measurements to account for noise in readings
    xvals = [window[i][0] for i in range(len(window))]
    yvals = [window[i][1] for i in range(len(window))]
    zvals = [window[i][2] for i in range(len(window))]

    return [mode(xvals), mode(yvals), mode(zvals)]


bvs = 1 #assume bay is vacant: 1; occupied: 0
while 1:
    #no adjustment for magnetic declination on the arduino
    #first run saves readings as previous reading without sending anything
    if isFirst:
        prv = get_window() #RUN TWICE to let readings settle
        prv = get_window()
        
        isFirst = not isFirst

    ################################
    #determine bay vacancy status
    ################################
    window = get_window()
    xchanged = (prv[0] - window[0]) != 0
    ychanged = (prv[1] - window[1]) != 0
    zchanged = (prv[2] - window[2]) != 0
    print("x: {} \t y: {} \t z: {}".format(window[0], window[1], window[2]))

    """
    Spend time learning the magnitude of change in raw axis readings when the bay is vacant
    or occupied to formulate a more robust bay status change condition.
    """

    #"calculate" the vacancy based on window
    if xchanged or ychanged or zchanged:
        print("bay status changed")
        #send bay vacancy status changed
        bvs = not bvs

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host, port = ipAddress, 65000 
    server_address = (host, port)

    #Pack three 32-bit floats into message and send
    message = pack('5f', bay, bvs, window[0], window[1], window[2])
    sock.sendto(message, server_address)

    #update previous readings with last reading
    prv = window

    sleep(1) #1sec