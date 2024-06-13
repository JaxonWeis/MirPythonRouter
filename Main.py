from time import sleep
import MIR
import RouterClass
import urx

# Create Robots
fleet = MIR.Fleet()
fleet.inductRobot("Mir 600", "192.168.1.5", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
fleet.inductRobot("Mir 250_1", "192.168.1.10", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
fleet.inductRobot("Mir 250_2", "192.168.1.15", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
fleet.inductRobot("Mir 250_3", "192.168.1.20", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")

router = RouterClass.Router()

for each in fleet.getBusyRobots():
    router.addCustomRoute(each, [])

rob = urx.Robot("192.168.1.25")



while True:
    print("--------------------------------------------------------")
    print(str(rob.get_pose()))
    sleep(5)


    '''
    # display all robot status
    fleet.update()
    fleet.printStatus()
    print()

    # print robot Status
    print("Waiting Robots: " + str(len(fleet.getWaitingRobots()))
          + "\tBusy Robots: " + str(len(fleet.getBusyRobots()))
          + "\tNeed Charging Robots: " + str(len(fleet.getNeedChargeRobots())))
    print()

    # print route queue
    router.printStatus()

    # print map
    router.printMap()

    # Match robot to route
    if fleet.hasRobotsWaiting() and router.hasRoutes():
        bot = fleet.getWaitingRobots()[0]
        if bot not in router.routeRunning:
            router.addRoute(bot)

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
    for bot in fleet.getWaitingRobots():
        if router.canContinue(bot):
            bot.postMissionByName(router.getNextLocation(bot, bot.location))

    for bot in fleet.getNeedChargeRobots():
        if router.canContinue(bot):
            bot.postMissionByName(router.getNextLocation(bot, bot.location))

    sleep(5)
    '''










