from time import sleep
import MIR
import RouterClass
import URModbus
import PLC

# Create MIR Robot Fleet
fleet = MIR.Fleet()
#fleet.inductRobot("MiR 600", "192.168.1.20", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
fleet.inductRobot("MiR 250_1", "192.168.1.21", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
# fleet.inductRobot("MiR 250_2", "192.168.1.22", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
# fleet.inductRobot("MiR 250_3", "192.168.1.23", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")

# Create UR Arm
UR20_1 = URModbus.URArm("UR20_1", "192.168.1.7")
UR20_1.setReady(True)
# Action 1 is Pick from Lane 3
# Action 2 is Pick from Mir Robot
# Action 3 is Place on Conveyor 1

UR20_2 = URModbus.URArm("UR20_2", "192.168.1.8")
UR20_2.setReady(True)
# Action 1 is Pick from Lane 1
# Action 2 is Place on Mir Robot

UR10_1 = URModbus.URArm("UR10_1", '192.168.1.12')

UR10_2 = URModbus.URArm("UR10_2", '192.168.1.13')


UR20_1.Dashboard.play()
UR20_2.Dashboard.play()
UR10_1.Dashboard.play()
UR10_2.Dashboard.play()


# Create PLC
PLC1 = PLC.PLC("192.168.1.10")
PLC1.updateLanes()
Lane1 = PLC1.lane1
Lane2 = PLC1.lane2
Lane3 = False

# Create Router
router = RouterClass.Router()
router.addToQueue(['MiR 250_1', 'UR2: Action 1', 'DropOff', 'UR2: Wait', 'UR2: Action 2', 'UR2: Wait',  'Pickup', 'UR1: Action 2', 'UR1: Action 3'])
router.addToQueue(['MiR 250_1', 'UR2: Action 1', 'DropOff', 'UR2: Wait', 'UR2: Action 2', 'UR2: Wait',  'Pickup', 'UR1: Action 2', 'UR1: Action 3'])
router.addToQueue(['MiR 250_1', 'UR2: Action 1', 'DropOff', 'UR2: Wait', 'UR2: Action 2', 'UR2: Wait',  'Pickup', 'UR1: Action 2', 'UR1: Action 3'])


while True:
    print("\n\n\nDASHBOARD###########################################################\n")

    # display MiR robot status
    print("MiR Robots:")
    fleet.update()
    fleet.printStatus()
    print()


    # Check PLC Status
    PLC1.updateLanes()
    print("PLC Info:")
    print("Lane1")
    print(PLC1.lane1)
    print("Lane2")
    print(PLC1.lane2)
    print("Lane3")
    print(PLC1.lane3)
    print()


    # Add Route Bases on PLC Status
    if PLC1.lane1 > Lane1:
        router.addToQueue(['MiR 250_1', 'UR2: Action 1', 'DropOff', 'UR2: Wait', 'UR2: Action 2', 'UR2: Wait',  'Pickup', 'UR1: Action 2', 'UR1: Action 3'])
        Lane1 = Lane1 + 1
    elif PLC1.lane1 < Lane1:
        Lane1 = PLC1.lane1
        
    if PLC1.lane2 > Lane2:
        #TODO
        Lane2 = Lane2 + 1
    elif PLC1.lane2 < Lane2:
        Lane2 = PLC1.lane2


    # print route queue
    router.printStatus()


    # print map
    router.printMap()


    # Match robot to route
    for bot in fleet.getWaitingRobots():
        if bot not in router.routeRunning:
            if router.hasRoutes():
                router.addRoute(bot, bot.name)


    # print running Queue
    router.printRunningQueue()
    
    print("____________________________________________________________________")

    # Assign Robots needing charge routes
    if fleet.hasRobotsNeedCharge():
        bot = fleet.getNeedChargeRobots()[0]
        if bot not in router.routeRunning:
            router.addCustomRoute(bot, ['Charge'])

    # Execute Running Queue
    for bot in fleet.getWaitingRobots() + fleet.getNeedChargeRobots():
        if router.canContinue(bot):
            location = router.getNextLocation(bot, bot.location)
            
            if "UR1" in location:
                if "Action 1" in location and UR20_1.isReady():
                    UR20_1.setAction(1)
                    router.removeNextLocation(bot)
                elif "Action 2" in location and UR20_1.isReady():
                    UR20_1.setAction(2)
                    router.removeNextLocation(bot)
                elif "Action 3" in location and UR20_1.isReady():
                    UR20_1.setAction(3)
                    router.removeNextLocation(bot)
                elif "Wait" in location and UR20_1.isReady():
                    router.removeNextLocation(bot)
            elif "UR2" in location:                
                if "Action 1" in location and UR20_2.isReady():
                    UR20_2.setAction(1)
                    router.removeNextLocation(bot)
                if "Action 2" in location and UR20_2.isReady():
                    UR20_2.setAction(2)
                    router.removeNextLocation(bot)
                elif "Wait" in location and UR20_2.isReady():
                    router.removeNextLocation(bot)
            else:
                bot.postMissionByName(location)
    
    # Pickup Lane3 if Full
    if PLC1.lane3 and UR20_1.isReady():
        UR20_1.setAction(1)
    
    sleep(5)










