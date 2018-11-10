import threading
import time
from logging import RootLogger

from typeguard import typechecked
from pydispatch import dispatcher

from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent


class AsyncJobsThread(threading.Thread):
    LISTEN_DELAY = 0.03

    @typechecked()
    def __init__(self, async_jobs: AsyncActuatorCommands, logging: RootLogger):
        threading.Thread.__init__(self)
        self.__async_jobs = async_jobs
        self.__logging = logging
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__async_jobs.listen(self.__job_callback)
            time.sleep(self.LISTEN_DELAY)

    def __job_callback(self, job_data):
        self.__logging.info('Incomming job data: {0}' .format(job_data))
        dispatcher.send(ChangeActuatorRequestEvent.NAME,
                        event=ChangeActuatorRequestEvent(job_data["actuator"], job_data["value"]))