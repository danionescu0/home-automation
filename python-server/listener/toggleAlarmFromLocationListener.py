import json
from blinker import signal
from geopy.distance import vincenty

class toggleAlarmFromLocationListener:
    def __init__(self, homeCoordonates, jobControll, locationTracker):
        self.__homeCoordonates = homeCoordonates
        self.__jobControll = jobControll
        self.__locationTracker = locationTracker
        self.__maxDistanceToTriggerSwitch = 0.2
        location = signal("location")
        location.connect(self.callback)

    def callback(self, location):
        actuatorState = False
        actuatorName = "homeAlarm"
        currentCoordonates = (location.getLatitude(), location.getLongitude())
        distanceFromHome = vincenty(self.__homeCoordonates, currentCoordonates)
        if distanceFromHome > self.__maxDistanceToTriggerSwitch:
            print "switched"
        # self.jobControll.addJob(json.dumps({"job_name": "actuators", "actuator": actuatorName, "state": actuatorState}))
        print(distanceFromHome)
