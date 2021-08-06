'''
Aaron Samuel
UCID: as3655
Section 012
'''
#! /usr/bin/env python3
# Echo Server
import sys
import socket
import random
import struct
# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + '\n')

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)
    message = struct.unpack("!II", data)
    x = random.randint(1, 10)

    if (x < 4):
        print('Message with Sequence Number ' + str(message[1]) + ' dropped')
    else:
        message2 = struct.pack('!II', 2, message[1])
        serverSocket.sendto(message2, address)
        print('Responding to Ping Request with Sequence Number ' + str(message[1]))
