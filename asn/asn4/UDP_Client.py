#version python3
#using "python3 UDP_Client.py" to run the code
import binascii
import socket
import struct
import sys
import hashlib
import time

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
sock.settimeout(0.009)
try:
	seq, addr = sock.recvfrom(1024)
	ack, addr = sock.recvfrom(1024)
	chksum, addr = sock.recvfrom(1024)

	#read the ack
	while ack == bytes(1) and seq == bytes(1) and UDP_Packet[3] != chksum:
		print("Fail to send package 1, resend package 1: (0, 0, b'NCC-1701', b'e4d48cc025bf08b68a1db367bb58e177')")
		sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

	else: #ack == bytes(0) and seq == bytes(0)
		print("CheckSums Match. Success sent package 1: (0, 0, b'NCC-1701', b'e4d48cc025bf08b68a1db367bb58e177')")
		print('Now sending package 2.')
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
		socket.timeout(0.009)
		try:
			seq, addr = sock.recvfrom(1024)
			ack, addr = sock.recvfrom(1024)
			chksum, addr = sock.recvfrom(1024)

			while ack == bytes(0) and seq == bytes(0) and UDP_Packet[3] != chksum:
				print("Fail to send package 2, resend package 2: (1, 1, b'NCC-1664', b'1133946b35e97fde8db689fd0fcb0a6c')")
				sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

			else:   #ack == bytes(1) and seq == bytes(1):	
				print("CheckSums Match. Success sent package 2: (1, 1, b'NCC-1664', b'1133946b35e97fde8db689fd0fcb0a6c')")
				print('Now sending package 3.')
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
				socket.timeout(0.009)
				try:
					seq, addr = sock.recvfrom(1024)
					ack, addr = sock.recvfrom(1024)
					chksum, addr = sock.recvfrom(1024)
		
					while ack == bytes(1) and seq == bytes(1) and UDP_Packet[3] != chksum:
						print("Fail to send package 3, resend package 3: (0, 0, b'NCC-1017', b'91403416ae18fd2ff3905deaa243e4d5')")
						sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
					else:   #ack == bytes(0) and seq == bytes(0):
					 	print("CheckSums Match. Success sent package 3: (0, 0, b'NCC-1017', b'91403416ae18fd2ff3905deaa243e4d5')")
					print('Success sent 3 packeges.')

#when sending package3, time out happened
				except socket.timeout:
					print ("Time out, resending package 3: (0, 0, b'NCC-1017', b'91403416ae18fd2ff3905deaa243e4d5') again.")
					sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
					while True:	
						print ("Time out, resending package 3: (0, 0, b'NCC-1017', b'91403416ae18fd2ff3905deaa243e4d5') again.")
						sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))


#when sending package2, time out happened
		except socket.timeout:
			print ("Time out, resending package 2: (1, 1, b'NCC-1664', b'1133946b35e97fde8db689fd0fcb0a6c') again.")
			sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
			while True:	
				print ("Time out, resending package 2: (1, 1, b'NCC-1664', b'1133946b35e97fde8db689fd0fcb0a6c') again.")
				sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

#when sending package1, time out happened
except socket.timeout: 
	print ("Time out, resending package 1: (0, 0, b'NCC-1701', b'e4d48cc025bf08b68a1db367bb58e177')again.")
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
	while True:	
		print ("Time out, resending package 1: (0, 0, b'NCC-1701', b'e4d48cc025bf08b68a1db367bb58e177') again.")
		sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
