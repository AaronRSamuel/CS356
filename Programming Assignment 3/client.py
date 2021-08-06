'''
Aaron Samuel
UCID: as3655
Section 012
'''
#! /usr/bin/env python3
# Echo Client
import sys
import socket
import struct
import random

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostname = sys.argv[3]
messageType = 1
returnCode = 0;
question = hostname + " A IN"
questionLen = len(question)
answer = ""
answerLen = len(answer)

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1.0);

for i in range(3):
    ident = random.randint(1, 100)
    try:
        message = struct.pack('!HHiHH' + str(questionLen) + 's', messageType, returnCode, ident, questionLen, answerLen, question.encode('ascii'))

    except struct.error:
        print("non ASCII characters can not be encoded")

    print("Sending Request to " + host + ", " + str(port) + ":")
    if (i == 0):
        print(
            "Message ID:   " + str(ident) + "\nQuestion Length: " + str(questionLen) + " bytes\nAnswer Length: " + str(answerLen) + " bytes\nQuestion: " + question)
    clientsocket.sendto(message, (host, port))

    rec = False
    try:
        MES, ad = clientsocket.recvfrom(1024)
        rec = True
        answerLen = struct.unpack('!H', MES[10:12])[0]
        messEcho = struct.unpack('!HHiHH' + str(questionLen) + 's' + str(answerLen) + 's', MES)

        if answerLen == 0:
            print("\nReceived response from " + str(host) + ", " + str(port) + ":\nReturn Code: " + str(messEcho[1]) + " (Name does not exist)\nMessage ID:   " + str(messEcho[2]) + "\nQuestion Length: " + str(
                messEcho[3]) + "bytes\nAnswer Length: " + str(messEcho[4]) + "bytes\nQuestion: " + messEcho[5].decode('ascii'))

        else:
            print("\nReceived response from " + str(host) + ", " + str(port) + ":\nReturn Code: " + str(messEcho[1]) +
                  "(No errors)\nMessage ID:   " + str(messEcho[2]) + "\nQuestion Length: " + str(messEcho[3]) +
                  "bytes\nAnswer Length: " + str(messEcho[4]) + "bytes\nQuestion: " + messEcho[5].decode('ascii') +"\nAnswer: " + messEcho[6].decode('ascii'))

    except socket.timeout:
        print("timed out")

    if rec:
        break