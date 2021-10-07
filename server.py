#!/usr/bin/env python3

#sourcce:https://stackoverflow.com/questions/64642122/how-to-send-real-time-sensor-data-to-pc-from-raspberry-pi-zero


import socket
import sys
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
	id, x, y, z = unpack('4f', message)
	print(f'id: {id}, X: {x}, Y: {y}, Z: {z}')
	

	if x > 5 and y > 5 and z > 5: #some condition to see if bay is occupied
		Bay.query.filter(Bay.bay_id == int(id)).update({'bay_status': 'occupied'})
		print('occupied')
		db.session.commit()
	else:
		Bay.query.get(int(id)).update({'bay_status': 'vacant'})
		print('vacant')
		db.session.commit()