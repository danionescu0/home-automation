from typeguard import typechecked
from pydispatch import dispatcher

from repository.ActuatorsRepository import ActuatorsRepository
from tools.EmailNotifier import EmailNotifier
from event.SensorUpdateEvent import SensorUpdateEvent
from model.Sensor import Sensor
from locking.HomeAlarmLock import HomeAlarmLock
from listener.BaseListener import BaseListener


class IntruderAlertListener(BaseListener):
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, email_notificator: EmailNotifier,
                 home_alarm_lock: HomeAlarmLock):
        self.__actuators_repo = actuators_repo
        self.__email_notificator = email_notificator
        self.__home_alarm_lock = home_alarm_lock

    def connect(self):
        dispatcher.connect(self.listen, signal=SensorUpdateEvent.NAME, sender=dispatcher.Any)

    def listen(self, event: SensorUpdateEvent) -> None:
        if False == self.__should_send_alert(event):
            return
        self.__email_notificator.send_alert("Alert", "Somebody entered the house")
        self.__home_alarm_lock.set_lock()

    def __should_send_alert(self, sensor_update: SensorUpdateEvent):
        if self.__home_alarm_lock.has_lock():
            return False
        actuators = self.__actuators_repo.get_actuators()

        return actuators['homeAlarm'].value == True \
               and sensor_update.sensor.type == Sensor.SensorType.PRESENCE.value and sensor_update.sensor.value == 1