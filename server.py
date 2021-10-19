#!/usr/bin/env python3

#source:https://stackoverflow.com/questions/64642122/how-to-send-real-time-sensor-data-to-pc-from-raspberry-pi-zero
#UDP server to receive data from raspberry pi

import socket
from struct import unpack
from app import app, db, Bay
from sqlalchemy.sql import func
from flask_migrate import Migrate
migrate = Migrate(app, db)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65000
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

while True:
	# Wait for message
	message, address = sock.recvfrom(4096)

	print(f'Received {len(message)} bytes:')
	id, bvs, x, y, z = unpack('5f', message)

	print(f'id: {id}, bvs:{bvs}, X: {x}, Y: {y}, Z: {z}')
	
	if bool(bvs): #assume bay is vacant: 1; occupied: 0
		Bay.query.filter(Bay.bay_id == int(id)).update({'bay_status': 'vacant'})
		print('bay changed to vacant')
		db.session.commit()
	else:
		Bay.query.filter(Bay.bay_id == int(id)).update({'bay_status': 'occupied'})
		print('bay changed to occupied')
		db.session.commit()