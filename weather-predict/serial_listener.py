import time
import sys


import config
from container import Container


container = Container()

serial_device = container.serial()

while True:
    # serial_device.listen(self.__sensor_from_text_factory.can_create, self.__sensor_callback)
    time.sleep(0.1)