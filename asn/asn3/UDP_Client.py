#version python3
#using "python3 UDP_Client.py" to run the code
import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

#Create the Checksum for package 1
values = (0,0,b'NCC-1701')
UDP_Data = struct.Struct('I I 8s')
packed_data = UDP_Data.pack(*values)
chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

#Build the UDP Packet 1
values = (0,0,b'NCC-1701',chksum)
UDP_Packet_Data = struct.Struct('I I 8s 32s')
UDP_Packet = UDP_Packet_Data.pack(*values)

#Send the UDP Packet 1
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

seq, addr = sock.recvfrom(1024)
ack, addr = sock.recvfrom(1024)
#read the ack
while ack == bytes(1) and seq == bytes(1):
	print('Fail to send package 1, resend it.')
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

else: #ack == bytes(0) and seq == bytes(0)
	print('Success to send package 1, send package 2.')
	#Create the Checksum for package 2
	values = (1,1,b'NCC-1664')
	UDP_Data = struct.Struct('I I 8s')
	packed_data = UDP_Data.pack(*values)
	chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

	#Build the UDP Packet 2
	values = (1,1,b'NCC-1664',chksum)
	UDP_Packet_Data = struct.Struct('I I 8s 32s')
	UDP_Packet = UDP_Packet_Data.pack(*values)

	#Send the UDP Packet 2
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
	seq, addr = sock.recvfrom(1024)
	ack, addr = sock.recvfrom(1024)

	while ack == bytes(0) and seq == bytes(0):
		print('Fail to send package 2, resend it.')
		sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

	else:   #ack == bytes(1) and seq == bytes(1):
		print('Success to send package 2, send package 3.')
		#Create the Checksum for package 3
		values = (0,0,b'NCC-1017')
		UDP_Data = struct.Struct('I I 8s')
		packed_data = UDP_Data.pack(*values)
		chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

		#Build the UDP Packet 3
		values = (0,0,b'NCC-1017',chksum)
		UDP_Packet_Data = struct.Struct('I I 8s 32s')
		UDP_Packet = UDP_Packet_Data.pack(*values)

		#Send the UDP Packet 3
		sock = socket.socket(socket.AF_INET, # Internet
  	    	             socket.SOCK_DGRAM) # UDP
		sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
		seq, addr = sock.recvfrom(1024)
		ack, addr = sock.recvfrom(1024)

		while ack == bytes(1) and seq == bytes(1):
				print('Fail to send package 3, resend it.')
				sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
		else:   #ack == bytes(0) and seq == bytes(0):
			 	print('Successfully sent 3 packages')