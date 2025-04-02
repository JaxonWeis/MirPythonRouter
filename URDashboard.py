import socket
from time import sleep


class URControl:
    def __init__(self, name, host):
        self.name = name
        self.host = host
        self.port = 29999

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect()
        self.getLoadedProgram()
        
        self.getReady()


    def receive(self):
        data = self.socket.recv(1024).decode()
        #print(data)
        return data

    def send(self, data):
        data = data + "\n"
        self.socket.send(data.encode())
        return self.receive()

    def connect(self):
        print("\t\tConnecting to " + self.name + "... ", end="")
        try:
            self.socket.connect((self.host, self.port))
            print("Success!")
            return True
        except:
            print("FAILED!")
            return False

    def getMode(self):
        return self.send("robotmode").replace("\n", "").replace("Robotmode: ", "")

    def getReady(self):
        print("\t\tGetting Ready...", end="")

        while True:
            status = self.getMode()
            
            if "POWER_OFF" in status:
                print("p", end="")
                self.send("power on")
                sleep(1)

            if "IDLE" in status:
                print("b", end="")
                self.send("brake release")
                sleep(5)

            if "RUNNING" in status:
                print(" Ready!")
                return

    def isProgramRunning(self):
        data = self.send("running")
        if "true" in data:
            return True
        else:
            return False

    def loadProgram(self, program):
        print("\t\tUR: " + self.name + " Loading Program: " + program)
        self.send("load " + program + ".urp")
        sleep(1)
        
    def getLoadedProgram(self):
        return self.send("get loaded program").replace("\n", "").replace("/programs/", "")

    def printStatus(self):
        print("Name: " + self.name, end="")
        print("\t --Status:" + self.getMode(), end="")
        print("\t --Program: " + self.getLoadedProgram(), end="")
        print("\t --Running:" + str(self.isProgramRunning()))
        
    def play(self):
        print("\t\tUR: " + self.name + " Starting Program.") 
        self.send("play")
        
    def stop(self):
        self.send("stop")
        
    def powerOff(self):
        self.send("power off")

    def shutdown(self):
        while self.isProgramRunning():
            sleep(1)
        self.send("shutdown")


'''
print("Starting.")
##########################################################
UR20_1 = URControl("UR20_1", '192.168.1.7')
UR20_1.printStatus()


print("\n\n\n")
##########################################################
UR20_2 = URControl("UR20_2", '192.168.1.8')
UR20_2.loadProgram("SignSpinner")
UR20_2.play()
UR20_2.printStatus()


print("\n\n\n")
##########################################################
UR10_1 = URControl("UR10_1", '192.168.1.12')
UR10_1.loadProgram("Demo")
UR10_1.play()
UR10_1.printStatus()

print("\n\n\n")
##########################################################
UR10_2 = URControl("UR10_2", '192.168.1.13')
UR10_2.loadProgram("Demo")
UR10_2.play()
UR10_2.printStatus()

sleep(30)

UR20_1.stop()
UR20_2.stop()
UR10_1.stop()
UR10_2.stop()

UR20_1.powerOff()
UR20_2.powerOff()
UR10_1.powerOff()
UR10_2.powerOff()
'''