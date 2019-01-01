import time
import datetime

from container import Container


container = Container()
serial_device = container.serial()
serial_device.connect()
sensor_builder = container.sensor_builder()
datapoint_repository = container.datapoints_repository()


while True:
    serial_device.listen(sensor_builder.add_text)
    if sensor_builder.is_complete():
        sensors = sensor_builder.build()
        datapoint_repository.update(datetime.datetime.now(), sensors)

    time.sleep(0.1)

serial_device.disconnect()