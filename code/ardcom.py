#!/usr/bin/env python

import serial


class Ardcom:
    def __init__(self, serial_port="/dev/ttyACM0", speed=1152000, timeout=2):
        self.timeout = timeout
        self.serial = serial.Serial(serial_port,speed, timeout = self.timeout)

    def send(self,data):
        """data is a string"""
        packet_size = len(data) + 2 #add two for the size header and checksum

        if packet_size > 255:
            raise Exception("Data size must not be greater than 253 bytes")

        checksum = int('00000000',2)
        for byte in data:
            checksum = checksum ^ ord(byte)
        checksum = chr(checksum)
        packet_size = chr(packet_size)

        packet = packet_size + data + checksum #construct the packet to send
        self.serial.write(packet)
        response = self.read_response()

        if response == "200":
            return
        elif response == "400":
            print "Corrupt packet read by arduino, resending"
            self.send(data) #fix this so we don't brutalise the stack if theres lots of broken packets
        else:
            raise Exception("Got unexpected response packet from Arduino: "+response)
            

    def read_response(self):
        #wait for response
        response_size = ord(self.serial.read())
        if response_size == 0:
            raise Exception("Arduino failed to respond within "+str(self.timeout)+" second timeout period")
        response_size = response_size - 1 #subtract the size of the header
        data = self.serial.read(size = response_size)
        #read the checksum for the hell of it
        checksum = int('00000000',2)
        for byte in data:
            checksum = checksum ^ ord(byte)
        if checksum != 0:
            print "read_response checksum error"

        return data[:-1] #cut off the checksum


data = [chr(int('00000001',2)),\
        chr(int('00000010',2)),\
        chr(int('00000001',2)),\
        chr(int('00000111',2))\
       ]

checksum = int('00000000',2)
for d in data:
    checksum = checksum ^ ord(d)
    print ord(d)
print "checksum " +str(checksum)
data.append(chr(checksum))

data = " ".join(data)

checksum = int('00000000',2)
for d in data:
    checksum = checksum ^ ord(d)
print "undone checksum "+str(checksum)
print data
