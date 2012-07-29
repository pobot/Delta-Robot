#!/usr/bin/env python

import serial
import time


def main():
    print "Running"
    comms = DeltaComms()
    comms.microstep = 8

    comms.delay = 0.0001


    while True:
        comms.sendCommands([(-1,-1,-1)]*200*8)
        comms.sendCommands([(1,1,1)]*200*8)


    comms.sendCommands([(-1,-1,-1)]*(200*8*4))
#    quit()
    comms.sendCommands([(1,1,1)]*(200*19))

    comms.sendCommands([(0,-1,0)]*(40))
    comms.sendCommands([(-1,0,0)]*(10))

#        quit()
#    comms.delay = 0.002
    while True:
        c = raw_input()
        if c != " ":
            comms.sendCommands([(1,1,1)]*(20))
#        time.sleep(1)
#        comms.sendCommands([(0,0,-1)]*(200*8))
#        quit()


    quit()
    while (True):
        command = raw_input("zyx: ")
        command.split()
        if len(command) != 3:
            continue
        x,y,z = command
        x = int(x)
        y = int(y)
        z = int(z)

        x_sign = 1
        y_sign = 1
        z_sign = 1

        comms.sendCommands([(-1,-1,-1)]*200)
        comms.sendCommands([(1,1,1)]*200)


class DeltaComms:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0",115200)
        time.sleep(2)
        self.microstep = 8
        self.delay = 0.0001

    def sendCommands(self,z_list):
        for z in z_list:
            self.sendCommand(z)

    def sendCommand(self,z):
        z0 = chr(0)
        z1 = chr(0)
        z2 = chr(0)

        microstep = chr(int('00000111',2))

        if self.microstep == 1:
            microstep = chr(int('00000000',2))
        if self.microstep == 2:
            microstep = chr(int('00000001',2))
        if self.microstep == 4:
            microstep = chr(int('00000010',2))
        if self.microstep == 8:
            microstep = chr(int('00000011',2))
        if self.microstep == 16:
            microstep = chr(int('00000111',2))

        if z[0] == 0:
            z0 = chr(int('00000000',2))
        if z[0] == 1:
            z0 = chr(int('00000001',2))
        if z[0] == -1:
            z0 = chr(int('00000010',2))

        if z[1] == 0:
            z1 = chr(int('00000000',2))
        if z[1] == 1:
            z1 = chr(int('00000001',2))
        if z[1] == -1:
            z1 = chr(int('00000010',2))

        if z[2] == 0:
            z2 = chr(int('00000000',2))
        if z[2] == 1:
            z2 = chr(int('00000001',2))
        if z[2] == -1:
            z2 = chr(int('00000010',2))

        self.ser.write(z0+z1+z2+microstep+'\n')
        time.sleep(self.delay)
            

if __name__ == "__main__":
    main()
    quit()

