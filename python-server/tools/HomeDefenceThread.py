import threading
import time

class HomeDefenceThread(threading.Thread):
    ITERATE_INTERVAL = 60

    def __init__(self, home_defence):
        threading.Thread.__init__(self)
        self.__home_defence = home_defence
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            time.sleep(self.ITERATE_INTERVAL)
            self.__home_defence.iterate_burgler_mode()