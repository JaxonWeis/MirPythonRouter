
class Router:

    def __init__(self):
        self.routeQueue = []
        self.routeQueue.append(['Spot1', 'Spot2', 'Spot3', 'Spot4', 'Spot5'])
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

    def addRoute(self, bot):
        self.routeRunning[bot] = self.routeQueue[0].copy()

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
                return False
        else:
            return False

    def getNextLocation(self, bot, lastLocation):
        if self.canContinue(bot):
            location = self.routeRunning[bot].pop(0)
            if location in self.map:
                self.map[location] = bot
            if lastLocation in self.map:
                self.map[lastLocation] = None
            if len(self.routeRunning[bot]) == 0:
                self.routeRunning.pop(bot)
            return location
        else:
            return ""
