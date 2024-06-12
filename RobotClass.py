import json, requests
class Robot:
    def __init__(self, name, ip, auth):
        self.ip = ip
        self.name = name
        self.auth = auth

        self.host = "http://" + self.ip + "/api/v2.0.0/"
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.headers["Authorization"] = auth

        self.missions = ""
        self.getMissions()
        self.missionNames = []
        self.getMissionNames()

        self.battery = 0
        self.status = ""

        self.location = ""
        self.getStatus()

    def __str__(self):
        return "Name: " + self.name

    def __repr__(self):
        return self.name

    def printStatus(self):
        status = self.getStatus()
        print ("Name: " + self.name + "\n-- Battery: " + str(status['battery_percentage']) + "\n-- Mission State: " + \
            status['state_text'] + "\n-- Location: " + self.location)

    def getMissions(self):
        self.missions = requests.get(self.host + "missions", headers=self.headers).json()
        return self.missions

    def getMissionNames(self):
        self.missionNames = []
        for each in self.missions:
            self.missionNames.append(each["name"])
        return self.missionNames

    def postMission(self, mission):
        mission_id = {"mission_id": mission}
        #print("*" + self.name + ": mission added " + mission_id)
        return requests.post(self.host + "mission_queue", json=mission_id, headers=self.headers)

    def postMissionByName(self, mission_name):
        mission_id = ""
        self.getMissions()
        for each in self.missions:
            if each["name"] == mission_name:
                mission_id = each["guid"]
        if mission_id != "":
            self.postMission(mission_id)
            self.location = mission_name
        print("**" + self.name + ": mission adding " + mission_name + "...**")

    def getMissionQueue(self):
        missionQueue = requests.get(self.host + "mission_queue", headers=self.headers).json()
        return missionQueue

    def getStatus(self):
        status = requests.get(self.host + "status", headers=self.headers).json()
        self.status = status['state_text']
        self.battery = status['battery_percentage']
        return status