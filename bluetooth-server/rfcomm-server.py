# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import os

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "823fc014-6ffa-4be6-accc-f1c342b23bae"
print "Using UUID:", uuid

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                    )
while True:           
	print "Waiting for connection on RFCOMM channel %d" % port

	client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info
	
	try:
		while True:
			data = client_sock.recv(1024)
			if len(data) == 0: break
			if data == "ping":
				client_sock.sendall("pong")
				print "received ping, responded w/ pong"
				os.system("python ../demo.py")
			else:
				print "received [%s]" % data
	
	except IOError:
		pass
	print "disconnected"	
	client_sock.close()
server_sock.close()
print "all done"
