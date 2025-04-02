# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 10:20:44 2024

@author: e8001685
"""

from pyModbusTCP.client import ModbusClient
from time import sleep
import URDashboard

class URArm:
    def __init__(self, name, host):
        self.name = name
        self.host = host
        print("Starting Connection To " + self.name + " @ " + self.host + "...")
        
        #Modbus server Setup
        print("\tStarting Modbus Server...", end="")
        self.connection = ModbusClient(host=self.host, port=502, auto_open=True, debug=False)
        if ( self.connection.open() ):
            print("\tSuccess!")
        else:
            print("\tFailed!!!")

        
        #Dashboard server setup
        print("\tStarting Dashboard Server...")
        self.Dashboard = URDashboard.URControl(self.name, self.host)
        self.Dashboard.loadProgram("Demo")
        print("\tDone!")
        
        self.writeBit(300, False)
        self.writeBit(301, False)
        self.writeBit(302, False)
        
        
        print("Done!!!\n")
        
        
    def wakeup(self):
        if not self.connection.is_open:
            self.connection.open()
            sleep(1)
    
    def writeBit(self, bit, status):
        # 300 is starting bit for boolean
        self.wakeup()
        loop = 0
        while not self.connection.write_single_coil(bit, status):
            print("Failed to send")
            loop = loop + 1
            if loop > 3:
                break
            sleep(1)

    def readBit(self, bit):
        # 500 is starting bit for boolean
        self.wakeup()
        return self.connection.read_coils(bit, 1)
    
    def setReady(self, status):
        print("Writing Ready Bit.")
        self.writeBit(300, status)

        if status == True:
            print("Waiting For Response...", end="")
            while not self.readBit(500):
                print(".", end="")
                sleep(1)
            print("ACK!")
        
    def setAction(self, num):
        action = num + 300
        ack = num + 500
        print("Writing bit to run Action.")
        self.writeBit(action, True)

        print("Waiting For Response...", end="")
        while self.readBit(ack) == [False]:
            print(".", end="")
            sleep(1)
        print("ACK!")
        self.writeBit(action, False)
        
    def isReady(self):
        ready0 = self.readBit(500) == [True]
        ready1 = self.readBit(501) == [False]
        ready2 = self.readBit(502) == [False]
        ready = ready0 and ready1 and ready2
        print(self.name + " is: " + str( ready ) )
        return ready
        


'''

UR20_1 = URArm("UR20_1", '192.168.1.7')
UR20_2 = URArm("UR20_2", '192.168.1.8')
UR10_1 = URArm("UR10_1", '192.168.1.12')
UR10_2 = URArm("UR10_2", '192.168.1.13')

print("UR Arm Ready!\n")

sleep(5)

#UR20_1.setReady(True)
#UR20_2.setReady(True)


UR20_1.Dashboard.shutdown()
UR20_2.Dashboard.shutdown()
UR10_1.Dashboard.shutdown()
UR10_2.Dashboard.shutdown()
'''

'''
UR20_1.writeBit(300, True)

while True:
    response = UR20_1.readBit(500)
    print(response)
    if response:
        break
    sleep(1)
'''    





'''
UR20_2.setAction(1)

print("Waiting for Robot to finish ...", end="")
while UR20_2.areActionsRunning():
    print(".", end="")
    sleep(1)
print("Done!")


UR20_1.setAction(2)


print("Waiting for Robot to finish ...", end="")
while UR20_1.areActionsRunning():
    print(".", end="")
    sleep(1)
print("Done!")

UR20_1.writeBit(300, False)
UR20_2.writeBit(300, False)
'''


    
        
        
        

