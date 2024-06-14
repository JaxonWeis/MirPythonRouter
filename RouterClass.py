
class Router:

    def __init__(self):
        self.routeQueue = []
        self.routeQueue.append(['any', 'Spot1', 'Spot2', 'Spot3', 'Spot4', 'Spot5'])
        self.routeRunning = {}
        self.map = {'Spot1': None, 'Spot2': None, 'Spot3': None, 'Spot4': None, 'Spot5': None, 'Charge1': None, 'Charge2': None}

    def printStatus(self):
        print("Route Queue: " + str(len(self.routeQueue)))
        for each in self.routeQueue:
            print(each)

        print()

    def printMap(self):
        print("Map:")
        for each in self.map:
            print(each + ": " + str(self.map[each]))
        print()

    def printRunningQueue(self):
        print("Routes Running: " + str(len(self.routeRunning)))
        for each in self.routeRunning:
            print(str(each) + ": " + str(self.routeRunning[each]))
        print()

    def addRoute(self, bot, name):
        for route in self.routeQueue:
            if route[0] == name or route[0] == 'any':
                print(route[0])
                if route[0] == 'any':
                    self.routeRunning[bot] = route.copy()
                else:
                    self.routeRunning[bot] = route.copy()
                    self.routeQueue.remove(route)
                self.routeRunning[bot].pop(0)
                break

    def addCustomRoute(self, bot, route):
        self.routeRunning[bot] = route

    def hasRoutes(self):
        return len(self.routeQueue) > 0

    def locationIsAvailable(self, location):
        return self.map[location] is None

    def canContinue(self, bot):
        if bot in self.routeRunning:
            if len(self.routeRunning[bot]) > 0:
                if self.routeRunning[bot][0] in self.map:
                    if self.map[self.routeRunning[bot][0]] is None:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                self.routeRunning.pop(bot)
                return False
        else:
            return False

    def getNextLocation(self, bot, lastLocation):
        location = self.routeRunning[bot][0]
        if "UR" in location:
            return location
        if location in self.map:
            self.map[location] = bot
        if lastLocation in self.map:
            self.map[lastLocation] = None
        self.routeRunning[bot].pop(0)
        return location

    def removeNextLocation(self, bot):
        self.routeRunning[bot].pop(0)

    def addToQueue(self, route):
        if route[0] == 'any':
            self.routeQueue.append(route)
        else:
            self.routeQueue.insert(0, route)
