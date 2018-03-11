import threading
import time
from logging import RootLogger

from typeguard import typechecked

from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.interpretter.InterpretterContext import InterpretterContext
from ifttt.command.CommandExecutor import CommandExecutor
from repository.IftttRulesRepository import IftttRulesRepository


class IftttRulesThread(threading.Thread):
    ITERATE_INTERVAL = 60

    @typechecked()
    def __init__(self, ifttt_rules: IftttRulesRepository, command_executor: CommandExecutor,
                 tokenizer: Tokenizer, logging: RootLogger):
        threading.Thread.__init__(self)
        self.__ifttt_rules = ifttt_rules
        self.__command_executor = command_executor
        self.__tokenizer = tokenizer
        self.__logging = logging
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__do_run()
            time.sleep(self.ITERATE_INTERVAL)

    def __do_run(self):
        rules = self.__ifttt_rules.get_all()
        for name, rule in rules.items():
            should_execute = self.__check_rule(rule.text)
            self.__logging.info('Checking rule: {0}, status is: {1}'
                                 .format(rule.text, {True: 'Ok', False: 'Not ok'}[should_execute]))
            if not rule.active or not should_execute:
                continue
            for command in rule.rule_commands:
                self.__command_executor.execute(command)

    def __check_rule(self, rule: str) -> bool:
        context = InterpretterContext()
        expression_builder = ExpressionBuilder(self.__tokenizer, self.__logging)
        expression_builder.set_text(rule)
        try:
            expression_builder.build()
        except Exception as e:
            self.__logging.error('Error building rule: {0}'.format(e.message))
            return False
        statement = expression_builder.get_expression()
        statement.interpret(context)

        return context.lookup(statement)