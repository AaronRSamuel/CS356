# Tyler Kim
# tk296
# CS 356-001

# *** Sources ***
# Unpacking bytestrings
# https://stackoverflow.com/questions/3753589/packing-and-unpacking-variable-length-array-string-using-the-struct-module-in-py
# Deleting empty lines
# https://stackoverflow.com/questions/2369440/how-to-delete-all-blank-lines-in-the-file-with-the-help-of-python

import sys, socket, struct

# Cline args
ip = sys.argv[1]
port = int(sys.argv[2])

# Prep file
resourceRecords = []
with open('dns-master.txt', 'r') as file:
    for line in file:
        if not line.isspace() and not line.startswith('#'):
            resourceRecords.append(line.rstrip())

# Create UDP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((ip, port))

print("The server is ready to receive on port: " + str(port) + "\n")

while True:
    # Receive data from client
    dataStructed, address = serverSocket.recvfrom(1024)

    # Unpack size of question to unpack correctly
    questionLength = struct.unpack('!H', dataStructed[8:10])[0]

    # Unpack rest
    data = struct.unpack('!HHiHH' + str(questionLength) + 's', dataStructed)
    messageType = 2
    returnCode = 1
    identifier = data[2]
    answerLength = data[4]
    question = data[5].decode('ascii')

    #print (messageType, returnCode, identifier, questionLength, answerLength, question)

    # Set answer
    answer = ""
    for item in resourceRecords:
        if question == item[0:len(question)]:
            answer = item.rstrip()
            answerLength = len(answer)
            returnCode = 0

    # Pack
    messageEcho = struct.pack('!HHiHH' + str(questionLength) + 's' + str(answerLength) +
                              's', messageType, returnCode, identifier, questionLength, answerLength,
                              question.encode('ascii'), answer.encode('ascii'))

    print("Responding to identifier: " + str(identifier))
    #serverSocket.sendto(messageEcho, address)