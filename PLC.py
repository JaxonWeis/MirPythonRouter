# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:47:47 2024

"""

from pycomm3 import LogixDriver
from time import sleep

#c = ModbusClient(host='192.168.1.10', port=502, auto_open=True, debug=False)


class PLC:
    def __init__(self, ip):
        self.ip = ip
        self.plc = LogixDriver(self.ip)
        self.plc.open()
        self.lane1 = 0
        self.lane2 = 0
        self.lane3 = False
        
    def updateLanes(self):
        try:
            if not self.plc.connected:
                self.plc.open()
                
            self.lane1 = self.plc.read('Lane1')[1].get('ACC')
            self.lane2 = self.plc.read('Lane2')[1].get('ACC')
            self.lane3 = not self.plc.read('dp16')[1]
        except Exception:
            print( "PLC Error!")
            
    def removeLane1(self):
        self.plc.write("Lane1_RM", True)
        sleep(5)
        self.plc.write("Lane1_RM", False)
        
    def removeLane2(self):
        self.plc.write("Lane2_RM", True)
        sleep(5)
        self.plc.write("Lane2_RM", False)
        
        
        
'''        

PLC1 = PLC("192.168.1.10")
tagList = PLC1.plc.get_tag_list()


PLC1.updateLanes()

print( "Lane1: " + str( PLC1.lane1 ) )
print( "Lane2: " + str( PLC1.lane2 ) )
print( "Lane3: " + str( PLC1.lane3 ) )

'''


'''
for item in tagList:
    if item['data_type_name'] == "BOOL":
        print( item['tag_name'] )
        print( item['data_type_name'] )
        print( item )
        print("")
'''
        
