from typeguard import typechecked
from blinker import signal

from repository.ActuatorsRepository import ActuatorsRepository
from tools.EmailNotifier import EmailNotifier
from event.SensorUpdateEvent import SensorUpdateEvent
from model.SensorType import SensorType

class IntruderAlertListener:
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, email_notificator: EmailNotifier):
        self.__actuators_repo = actuators_repo
        self.__email_notificator = email_notificator
        signal("sensor_update").connect(self.callback)

    @typechecked()
    def callback(self, sensor_update: SensorUpdateEvent) -> None:
        if self.__should_send_alert(sensor_update):
            self.__email_notificator.send_alert("Alert", "Somebody entered the house")

    def __should_send_alert(self, sensor_update):
        actuators = self.__actuators_repo.get_actuators()
        sensor_type = sensor_update.get_type()
        sensor_value = sensor_update.get_new_value()

        return actuators['homeAlarm'].state == True and sensor_type == SensorType.PRESENCE.value and sensor_value == 1