#!/usr/bin/env python3

#source:https://stackoverflow.com/questions/64642122/how-to-send-real-time-sensor-data-to-pc-from-raspberry-pi-zero
#Client code to send data to UDP server
#to be run on raspberry pi

import socket
import sys
from time import sleep
import random
from struct import pack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '192.168.1.116', 65000 #static ip of server
server_address = (host, port)

# Generate some mock magneto values
bay, x, y, z = 1, 6.000, 6.323, 6.1243

# Pack into message and send
message = pack('4f', bay, x, y, z)
sock.sendto(message, server_address)
