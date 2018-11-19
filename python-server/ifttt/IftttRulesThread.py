import threading
import time
from logging import RootLogger

from typeguard import typechecked

from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.interpretter.InterpretterContext import InterpretterContext
from ifttt.command.CommandExecutor import CommandExecutor
from repository.IftttRulesRepository import IftttRulesRepository
from locking.RuleLock import RuleLock
from model.Rule import Rule


class IftttRulesThread(threading.Thread):
    ITERATE_INTERVAL = 5

    @typechecked()
    def __init__(self, ifttt_rules: IftttRulesRepository, command_executor: CommandExecutor,
                 tokenizer: Tokenizer, rule_lock: RuleLock, logging: RootLogger):
        threading.Thread.__init__(self)
        self.__ifttt_rules = ifttt_rules
        self.__command_executor = command_executor
        self.__tokenizer = tokenizer
        self.__rule_lock = rule_lock
        self.__logging = logging
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__do_run()
            time.sleep(self.ITERATE_INTERVAL)

    def __do_run(self):
        rules = self.__ifttt_rules.get_all()
        for name, rule in rules.items():
            should_execute = self.__check_rule(rule)
            self.__logging.info('Checking rule: {0}, status is: {1}'
                                 .format(rule.text, {True: 'Ok', False: 'Not ok'}[should_execute]))
            if not rule.active or not should_execute:
                continue
            self.__rule_lock.set_lock(rule)
            for command in rule.rule_commands:
                self.__command_executor.execute(command)

    def __check_rule(self, rule: Rule) -> bool:
        if self.__rule_lock.has_lock(rule):
            return False
        context = InterpretterContext()
        expression_builder = ExpressionBuilder(self.__tokenizer, self.__logging)
        expression_builder.set_text(rule.text)
        try:
            expression_builder.build()
        except Exception as e:
            self.__logging.error('Error building rule: {0}'.format(str(e)))
            return False
        statement = expression_builder.get_expression()
        statement.interpret(context)

        return context.lookup(statement)