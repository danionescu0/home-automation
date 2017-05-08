import threading
import time
from typeguard import typechecked

from tools.HomeDefence import HomeDefence

class HomeDefenceThread(threading.Thread):
    ITERATE_INTERVAL = 60

    @typechecked()
    def __init__(self, home_defence: HomeDefence):
        threading.Thread.__init__(self)
        self.__home_defence = home_defence
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            time.sleep(self.ITERATE_INTERVAL)
            self.__home_defence.iterate_burgler_mode()