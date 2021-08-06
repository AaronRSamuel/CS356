'''
Aaron Samuel
UCID: as3655
Section 012
'''
#! /usr/bin/env python3
# Echo Server
import sys
import socket
import struct
# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

filerec = []
with open('dns-master.txt', 'r') as file:
    for line in file:
        if not line.isspace() and not line.startswith('#'):
            filerec.append(line.rstrip())

print("The server is ready to receive on port:  " + str(serverPort) + '\n')

while True:
    data, address = serverSocket.recvfrom(1024)
    questionLen = struct.unpack('!H', data[8:10])[0]

    data = struct.unpack('!HHiHH' + str(questionLen) + 's', data)
    messageType = 2
    returnCode = 1
    iden = data[2]
    answerLen = data[4]
    question = data[5].decode('ascii')

    answer = ""
    for item in filerec:
        if question == item[0:len(question)]:
            answer = item.rstrip()
            answerLen = len(answer)
            returnCode = 0

    messageEcho = struct.pack('!HHiHH' + str(questionLen) + 's' + str(answerLen) + 's', messageType, returnCode, iden, questionLen, answerLen, question.encode('ascii'), answer.encode('ascii'))

    print("Responding to identifier: " + str(iden))
    serverSocket.sendto(messageEcho, address)