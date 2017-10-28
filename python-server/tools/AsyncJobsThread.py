import threading
import time
from logging import RootLogger

from typeguard import typechecked

from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent


class AsyncJobsThread(threading.Thread):
    LISTEN_DELAY = 0.03

    @typechecked()
    def __init__(self, async_jobs: AsyncActuatorCommands, change_actuator_request_event: ChangeActuatorRequestEvent,
                 logging: RootLogger):
        threading.Thread.__init__(self)
        self.__async_jobs = async_jobs
        self.__change_actuator_request_event = change_actuator_request_event
        self.__logging = logging
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__async_jobs.listen(self.__job_callback)
            time.sleep(self.LISTEN_DELAY)

    def __job_callback(self, job_data):
        self.__logging.debug('Incomming job data: {0}' .format(job_data))
        self.__change_actuator_request_event.send(job_data["actuator"], job_data["state"])