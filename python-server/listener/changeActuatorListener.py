from blinker import signal

class changeActuatorListener:
    def __init__(self, brain):
        self.__brain = brain
        actuatorChangedRequest = signal("actuator_changed_request")
        actuatorChangedRequest.connect(self.callback)

        print "actuator changed req listener registred"

    def callback(self, actuatorChangedRequest):
        print "actuator changed req"
        self.__brain.changeActuator(actuatorChangedRequest.getName(), actuatorChangedRequest.getNewState())
