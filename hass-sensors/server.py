import argparse
from time import sleep

from MqttConnection import MqttConnection
from Multisensor import Multisensor
from Serial import Serial


parser = argparse.ArgumentParser()
parser.add_argument('serial_port')
parser.add_argument('mqtt_host')
args = parser.parse_args()


serial = Serial(args.serial_port, 9600)
mqtt = MqttConnection(args.mqtt_host)
multisensor = Multisensor(mqtt)
serial.add_callback(multisensor.process_sensor)
serial.connect()
mqtt.connect()


while True:
    serial.loop()
    mqtt.loop()
    sleep(0.05)