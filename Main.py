from time import sleep
import RobotClass
import RouterClass
import urx

# Create Robots
mir600 = RobotClass.Robot("Mir 600", "192.168.1.5", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
mir250_1 = RobotClass.Robot("Mir 250_1", "192.168.1.10", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
mir250_2 = RobotClass.Robot("Mir 250_2", "192.168.1.15", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")
mir250_3 = RobotClass.Robot("Mir 250_3", "192.168.1.20", "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==")

allRobots = [mir600 , mir250_1, mir250_2, mir250_3]
# allRobots = [mir250_1, mir250_3]
waitRobots = []
activeRobots = []
chargingRobots = []

router = RouterClass.Router()

for each in allRobots:
    if each.status != "Ready":
        activeRobots.append(each)
        router.routeRunning[each] = []
    else:
        waitRobots.append(each)

while True:
    print("--------------------------------------------------------")

    # display all robot status
    for each in allRobots:
        each.printStatus()
    print()

    # sort robots by battery status
    index = 0
    loop = len(waitRobots)
    while index < loop:
        bot = waitRobots.pop(0)
        if bot.battery < 20:
            chargingRobots.append(bot)
        else:
            waitRobots.append(bot)
        index += 1

    # print robot Status
    print("Waiting Robots: " + str(len(waitRobots))
          + "\tActive Robots: " + str(len(activeRobots))
          + "\tNeed Charging Robots: " + str(len(chargingRobots)))
    print()

    # print route queue
    router.printStatus()

    # Match robot to route
    if (len(waitRobots) > 0) and router.hasRoutes():
        bot = waitRobots.pop(0)
        activeRobots.append(bot)
        router.addRoute(bot)

    if len(chargingRobots) > 0:
        if router.locationIsAvailable('Charge1'):
            bot = chargingRobots.pop(0)
            activeRobots.append(bot)
            router.addCustomRoute(bot, ['Charge1', 'Park'])
        elif router.locationIsAvailable('Charge2'):
            bot = chargingRobots.pop(0)
            activeRobots.append(bot)
            router.addCustomRoute(bot, ['Charge2', 'Park'])

    # print map
    router.printMap()

    # print running Queue
    router.printRunningQueue()

    # Execute Running Queue
    for each in activeRobots:
        if each.status == "Ready":
            if router.canContinue(each):
                each.postMissionByName(router.getNextLocation(each, each.location))

    for each in activeRobots:
        if each not in router.routeRunning:
            activeRobots.pop(activeRobots.index(each))
            waitRobots.append(each)

    sleep(2)











