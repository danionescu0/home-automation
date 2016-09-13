import threading
import time

from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.interpretter.InterpretterContext import InterpretterContext
from repository.IftttRules import IftttRules
from ifttt.parser.ParseException import ParseException

class IftttRulesThread(threading.Thread):
    def __init__(self, ifttt_rules, change_actuator_request_event, sensors_repo, actuators_repo, logging):
        threading.Thread.__init__(self)
        self.__ifttt_rules = ifttt_rules
        self.__change_actuator_request_event = change_actuator_request_event
        self.__sensors_repo = sensors_repo
        self.__actuators_repo = actuators_repo
        self.__logging = logging
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__do_run()

    def __do_run(self):
        while True:
            time.sleep(60)
            rules = self.__ifttt_rules.get_all_active()
            for key, rule in rules.iteritems():
                self.__logging.debug('Checking rule {0}'.format(key))
                if not self.__check_rule(rule[IftttRules.DATA]):
                    continue
                self.__logging.debug('Changing actuator {0} to state {1}'.format(rule['actuator'], rule['state']))
                self.__change_actuator_request_event.send(rule['actuator'], rule['state'])


    def __check_rule(self, rule):
        context = InterpretterContext()
        expression_builder = ExpressionBuilder(Tokenizer(), self.__sensors_repo, self.__actuators_repo)
        expression_builder.set_text(rule)
        try:
            expression_builder.build()
        except ParseException as e:
            self.__logging.debug('Error parsing rule: {0}' + e.message)
            return False
        statement = expression_builder.get_expression()
        statement.interpret(context)

        return context.lookup(statement)