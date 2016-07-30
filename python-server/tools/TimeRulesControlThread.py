import threading
import time

class TimeRulesControlThread(threading.Thread):
    def __init__(self, time_rules, change_actuator_request_event, logging):
        threading.Thread.__init__(self)
        self.__time_rules = time_rules
        self.__change_actuator_request_event = change_actuator_request_event
        self.__logging = logging
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__do_run()

    def __do_run(self):
        while True:
            time.sleep(60)
            rules = self.__time_rules.get_rules_that_match()
            for key, rule in rules.iteritems():
                self.__logging.debug('Changing actuator {0} to state {1}'.format(rule['actuator'], rule['state']))
                self.__change_actuator_request_event.send(rule['actuator'], rule['state'])