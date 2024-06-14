import socket
from time import sleep


class URArm:
    def __init__(self, name, host):
        self.name = name
        self.host = host
        self.port = 29999

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connected = False

        self.mode = ""

        self.programLoaded = "None"
        self.programRunning = False

        self.connect()
        self.getReady()

        self.readyToLoad = True
        self.readyToUnload = False

    def receive(self):
        data = self.socket.recv(1024).decode()
        return data

    def send(self, data):
        data = data + "\n"
        self.socket.send(data.encode())
        return self.receive()

    def connect(self):
        self.socket.connect((self.host, self.port))
        data = self.receive()
        if "Connected" in data:
            self.connected = True
            return True
        else:
            self.connected = False
            return False

    def getMode(self):
        self.mode = self.send("robotmode").replace("\n", "").replace("Robotmode: ", "")
        return self.mode

    def getReady(self):
        if not self.connected:
            return
        while True:
            status = self.getMode()

            if "POWER_OFF" in status:
                self.send("power on")

            if "IDLE" in status:
                self.send("brake release")

            if "RUNNING" in status:
                return

    def isProgramRunning(self):
        data = self.send("running")
        if "true" in data:
            self.programRunning = True
            return True
        else:
            self.programRunning = False
            return False

    def loadProgram(self, program):
        self.programLoaded = program
        self.send("load " + program + ".urp")

    def loadTruck(self):
        self.loadProgram("Load")
        self.send("play")
        self.readyToLoad = False
        self.readyToUnload = True
        self.inQueue = False

    def unloadTruck(self):
        self.loadProgram("Unload")
        self.send("play")
        self.readyToLoad = True
        self.readyToUnload = False
        self.inQueue = False

    def printStatus(self):
        print("Name: " + self.name +
              "\t --Status:" + self.mode +
              "\t --Program: " + self.programLoaded +
              "-" + str(self.programRunning) +
              "\t --ReadyToLoad: " + str(self.readyToLoad) +
              "\t --ReadyToUnload: " + str(self.readyToUnload))

    def update(self):
        self.isProgramRunning()
        self.getMode()

    def shutdown(self):
        while self.isProgramRunning():
            sleep(1)
        self.send("shutdown")
