#python version 3.5
#run the file by using "python3 Python_Client.py"

import socket
import time

serverName = '192.168.56.101'
serverPort = 12000

print ("Attempting to contact server at ",serverName,":",serverPort)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Client connects to server
clientSocket.connect((serverName, serverPort))
print ("Connection to Server Established")

#give a clue "Input your request: " to let user enter an ASCII request "What is the current date and time? "
request = input("Input your request: ")
#Send the input request to the server
clientSocket.sendto(request.encode(),(serverName, serverPort))
currentTime = clientSocket.recv(1024)

#receive the data about the current time from the server
#if current time is null, then print ERROR
if currentTime.decode() == '':
	print ("Error: Invalid request! Please send another connection and request!")
else:
#else, print the current time
	print (currentTime.decode())
#client closes connection, server stays running listening for next connection	
clientSocket.close()
