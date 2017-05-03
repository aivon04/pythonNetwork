#python version 3.5
#run the file by using "python3 Python_Server.py"

import socket
import datetime

serverName = '192.168.56.101'
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Server establishes connection
serverSocket.bind((serverName, serverPort))
#Server listens for incoming client requests
serverSocket.listen(5)
print ("The server is ready to receive")

while 1:
	#Server establishes connection with client
	connectionSocket, addr = serverSocket.accept()
	print('Server Address:', serverName)
	print('Client Address:', addr)
	print("Connection to Client Established")
	
	#Server receives the request from client
	request = connectionSocket.recv(1024)
	#transfer the sentence without " "
	request1 = set(request.decode().split(' '))
	originRequest = 'What is the current date and time?'
	request2 = set(originRequest.split(' '))
	#comparing the two sentences
	if request1 == request2:
		#if they are equal, then server responds with "Current Date and Time – 00/00/0000 00:00:00"
		currentTime = "Current Date and Time - %s" % datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
		#sending this to client
		connectionSocket.send(currentTime.encode())		
	else:
		#if they are not equal, then print ERROR
		print ("Error: Please send another connection and request!")
		#client closes connection, server stays running listening for next connection	
	connectionSocket.close()
