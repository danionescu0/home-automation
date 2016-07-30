import threading
import time

class HomeDefenceThread(threading.Thread):
    def __init__(self, home_defence):
        threading.Thread.__init__(self)
        self.__home_defence = home_defence
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__do_run()

    def __do_run(self):
        while True:
            time.sleep(60)
            self.__home_defence.iterate_burgler_mode()