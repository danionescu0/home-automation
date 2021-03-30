FROM python:3.8-buster

RUN apt-get update
RUN apt install git -y

WORKDIR /usr/local/bin/

RUN git clone https://github.com/danionescu0/home-automation.git home-automation

WORKDIR /usr/local/bin/home-automation/hass-sensors

RUN pip install -qr requirements.txt

ENV MQTT_SERVER=localhost

ENV SERIAL_PORT=/dev/ttyUSB0

CMD python ./server.py ${SERIAL_PORT} ${MQTT_SERVER}