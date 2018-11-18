from typeguard import typechecked

from locking.TimedLock import TimedLock
from model.Rule import Rule


class RuleLock:
    __LOCK_KEY = 'rule_lock_{0}'

    @typechecked()
    def __init__(self, timed_lock: TimedLock) -> None:
        self.__timed_lock = timed_lock

    @typechecked()
    def has_lock(self, rule: Rule) -> bool:
        return self.__timed_lock.has_lock(self.__get_lock_name(rule))

    @typechecked()
    def set_lock(self, rule: Rule) -> None:
        self.__timed_lock.set_lock(self.__get_lock_name(rule), rule.lock_after_activation)

    def __get_lock_name(self, rule: Rule) -> str:
        return self.__LOCK_KEY.format(rule.id)