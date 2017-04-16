import threading
import json
import time

class JobControlThread(threading.Thread):
    LISTEN_DELAY = 0.01

    def __init__(self, job_controll, change_actuator_request_event, logging):
        threading.Thread.__init__(self)
        self.__job_controll = job_controll
        self.__change_actuator_request_event = change_actuator_request_event
        self.__logging = logging
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__job_controll.listen(self.__job_callback)
            time.sleep(self.LISTEN_DELAY)

    def __job_callback(self, job_data):
        self.__logging.debug('Incomming job data: {0}' .format(job_data))
        job_data = json.loads(job_data)
        if job_data["job_name"] == "actuators":
            self.__change_actuator_request_event.send(job_data["actuator"], job_data["state"])