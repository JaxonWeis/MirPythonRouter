# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:37:53 2025

@author: e8001685
"""

import URModbus

shutdown = False



# Create UR Arm
UR20_1 = URModbus.URArm("UR20_1", "192.168.1.7")
UR20_1.setReady(True)

UR20_2 = URModbus.URArm("UR20_2", "192.168.1.8")
UR20_2.setReady(True)

UR10_1 = URModbus.URArm("UR10_1", '192.168.1.12')

UR10_2 = URModbus.URArm("UR10_2", '192.168.1.13')


print("Power Down")
UR20_1.Dashboard.powerOff()
UR20_2.Dashboard.powerOff()
UR10_1.Dashboard.powerOff()
UR10_2.Dashboard.powerOff()

if shutdown:
    UR20_1.Dashboard.shutdown()
    UR20_2.Dashboard.shutdown()
    UR10_1.Dashboard.shutdown()
    UR10_2.Dashboard.shutdown()    