import json
from blinker import signal
from geopy.distance import vincenty

class ToggleAlarmFromLocationListener:
    def __init__(self, home_coordonates, job_controll, locationTracker):
        self.__homeCoordonates = home_coordonates
        self.__job_controll = job_controll
        self.__locationTracker = locationTracker
        self.__maxDistanceToTriggerSwitch = 0.5
        location = signal("location")
        location.connect(self.callback)

    def callback(self, location):
        actuatorState = False
        actuatorName = "homeAlarm"
        currentCoordonates = (location.get_latitude(), location.get_longitude())
        distanceFromHome = vincenty(self.__homeCoordonates, currentCoordonates)
        if distanceFromHome > self.__maxDistanceToTriggerSwitch:
            print "switched"
        # self.__job_controll.add_job(json.dumps({"job_name": "actuators", "actuator": actuatorName, "state": actuatorState}))
        print(distanceFromHome)
