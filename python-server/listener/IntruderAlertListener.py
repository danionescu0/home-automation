from typeguard import typechecked
from blinker import signal

from repository.ActuatorsRepository import ActuatorsRepository
from tools.EmailNotifier import EmailNotifier
from event.SensorUpdateEvent import SensorUpdateEvent
from model.SensorType import SensorType
from locking.HomeAlarmLock import HomeAlarmLock


class IntruderAlertListener:
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, email_notificator: EmailNotifier,
                 home_alarm_lock: HomeAlarmLock):
        self.__actuators_repo = actuators_repo
        self.__email_notificator = email_notificator
        self.__home_alarm_lock = home_alarm_lock
        signal("sensor_update").connect(self.callback)

    @typechecked()
    def callback(self, sensor_update: SensorUpdateEvent) -> None:
        if False == self.__should_send_alert(sensor_update):
            return
        self.__email_notificator.send_alert("Alert", "Somebody entered the house")
        self.__home_alarm_lock.set_lock()

    def __should_send_alert(self, sensor_update):
        if self.__home_alarm_lock.has_lock():
            return False
        actuators = self.__actuators_repo.get_actuators()
        sensor_type = sensor_update.get_type()
        sensor_value = sensor_update.get_new_value()

        return actuators['homeAlarm'].value == True and sensor_type == SensorType.PRESENCE.value and sensor_value == 1