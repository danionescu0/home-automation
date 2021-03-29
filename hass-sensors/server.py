import atexit
import argparse
from time import sleep

from MqttConnection import MqttConnection
from Multisensor import Multisensor
from Serial import Serial
from LoggingConfig import LoggingConfig


parser = argparse.ArgumentParser()
parser.add_argument('serial_port')
parser.add_argument('mqtt_host')
args = parser.parse_args()

serial_baud = 9600
message_terminator = "|"

logging_config = LoggingConfig()
logger = logging_config.get_logger()
serial = Serial(args.serial_port, serial_baud, message_terminator, logger)
mqtt = MqttConnection(args.mqtt_host, logger)
multisensor = Multisensor(mqtt, logger)
serial.add_callback(multisensor.process_sensor)
serial.connect()
mqtt.connect()
multisensor.init_discovery()


def exit_handler():
    serial.disconnect()

atexit.register(exit_handler)


while True:
    serial.loop()
    mqtt.loop()
    sleep(0.05)