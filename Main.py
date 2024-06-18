from time import sleep
import MIR
import RouterClass
import UR


# Create MIR Robot Fleet
fleet = MIR.Fleet()
fleet.inductRobot("MiR 600", "192.168.1.5", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
fleet.inductRobot("MiR 250_1", "192.168.1.10", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
fleet.inductRobot("MiR 250_2", "192.168.1.15", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
fleet.inductRobot("MiR 250_3", "192.168.1.20", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")

# Create UR Arm
UR20 = UR.URArm("UR20", "192.168.1.25")

# Create Router
router = RouterClass.Router()

while True:
    print("--------------------------------------------------------")

    # display MiR robot status
    print("MiR Robots:")
    fleet.update()
    fleet.printStatus()
    print()

    # print Mir Robot Groups
    print("Waiting Robots: " + str(len(fleet.getWaitingRobots()))
          + "\tBusy Robots: " + str(len(fleet.getBusyRobots()))
          + "\tNeed Charging Robots: " + str(len(fleet.getNeedChargeRobots())))
    print()

    # display UR Robots
    print("UR Robots")
    UR20.update()
    UR20.printStatus()
    print()

    # Add route if UR is ready
    if UR20.readyToLoad:
        router.addToQueue(['MiR 250_1', 'Spot1', 'Spot2', 'Spot3', 'UR: Load', 'UR: Wait', 'Spot4', 'Spot5'])
        UR20.readyToLoad = False
    if UR20.readyToUnload:
        router.addToQueue(['MiR 250_1', 'Spot1', 'Spot2', 'Spot3', 'UR: Unload', 'UR: Wait', 'Spot4', 'Spot5'])
        UR20.readyToUnload = False

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

    # Assign Robots needing charge routes
    if fleet.hasRobotsNeedCharge():
        bot = fleet.getNeedChargeRobots()[0]
        if bot not in router.routeRunning:
            if router.locationIsAvailable('Charge1'):
                router.addCustomRoute(bot, ['Charge1', 'Park'])
            elif router.locationIsAvailable('Charge2'):
                router.addCustomRoute(bot, ['Charge2', 'Park'])

    # Execute Running Queue
    for bot in fleet.getWaitingRobots() + fleet.getNeedChargeRobots():
        if router.canContinue(bot):
            location = router.getNextLocation(bot, bot.location)
            if location == "UR: Load":
                UR20.loadTruck()
                router.removeNextLocation(bot)
            elif location == "UR: Unload":
                UR20.unloadTruck()
                router.removeNextLocation(bot)
            elif location == "UR: Wait":
                if not UR20.isProgramRunning():
                    router.removeNextLocation(bot)
            else:
                bot.postMissionByName(location)

    sleep(2)










