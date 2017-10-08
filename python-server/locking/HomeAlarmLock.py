from locking.TimedLock import TimedLock


class HomeAlarmLock():
    __LOCK_KEY = 'home_alarm_lock'

    def __init__(self, timed_lock: TimedLock, lock_duration: int) -> None:
        self.__timed_lock = timed_lock
        self.__lock_duration = lock_duration

    def has_lock(self) -> bool:
        return self.__timed_lock.has_lock(self.__LOCK_KEY)

    def set_lock(self) -> None:
        self.__timed_lock.set_lock(self.__LOCK_KEY, self.__lock_duration)