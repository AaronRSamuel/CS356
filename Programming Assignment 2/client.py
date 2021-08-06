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
import time

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
dataLength = 1000000
RTTList = []
totalPings = 0
numReceived = 0
numLost = 0

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1.0);


print('Pining ' + str(port) + ',' + str(port) + ':')
for i in range(10):
    message = struct.pack("!II", 1, i + 1)
    staRTTime = int(round(time.time() * 1000000))
    clientsocket.sendto(message, (host, port))
    try:
        dataEcho, address = clientsocket.recvfrom(dataLength)
        endTime = int(round(time.time() * 1000000))
        numReceived = numReceived + 1
    except Exception as e:
        print('Ping message number ' + str(i+1) + ' timed out.')
        numLost = numLost +1
        continue

    RTT = endTime - staRTTime
    RTT = RTT / 1000000
    RTT = round(RTT, 6)
    RTTList.append(RTT)

    totalPings = totalPings + 1
    print('Ping message number' + str(i + 1) + ' RTT: ' + str(RTT) + 'seconds')


print('Stats')
print('Total pacekts send:' + str(totalPings))
print('Recieved' + str(numReceived))
print('Lost' + str(numLost))

if (numReceived > 1):
    # percentLossed = (numLost / totalPings) * 100
    percentLossed = (numLost / 10) * 100
    print("Percent Lossed: " + str(percentLossed) + "%")
else:
    print("Percent Lossed: 0%")

print('Min RTT', min(RTTList), 'secs')
print('Max RTT', max(RTTList), 'secs')
print('Average RTT', sum(RTTList) / len(RTTList), 'secs')
print('Connection closed')
#Close the client socket
clientsocket.close()
