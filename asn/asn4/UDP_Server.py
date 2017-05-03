#version python3
#using "python3 UDP_Server.py" to run the code
import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
unpacker = struct.Struct('I I 8s 32s')
num = 0

#Create the socket and listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)
    print("received from:", addr)
    print("received message:", UDP_Packet)
    #Create the Checksum for comparison
    values = (UDP_Packet[0],UDP_Packet[1],UDP_Packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    #Compare Checksums to test for corrupt data
    if UDP_Packet[3] == chksum:
        print('CheckSums Match, Packet OK')
        if UDP_Packet[1] != num % 2:
            print('Detect duplicate, already got package',UDP_Packet[1],', now sending ack',UDP_Packet[0],'again.')
        else:
            #if okay, then send to client ack
            seq = bytes(UDP_Packet[1])
            ack = bytes(UDP_Packet[0])
            print('Successful received package ',UDP_Packet[1],', now sending ack ',UDP_Packet[0])
            sock.sendto(seq, addr)
            sock.sendto(ack, addr)
            sock.sendto(chksum, addr)
            num = num + 1
    else:
        print('Checksums Do Not Match, Packet Corrupt')
        #if not okay, then send to client last ack
        ack = bytes((UDP_Packet[0]+1)%2)
        seq = bytes((UDP_Packet[1]+1)%2)
        print('Fail..did not receive package ',UDP_Packet[1],', now sending ack ',(UDP_Packet[0]+1)%2, 'again.')
        sock.sendto(seq, addr)
        sock.sendto(ack, addr)
        sock.sendto(chksum, addr)




