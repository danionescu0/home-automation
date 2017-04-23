import serial

from communication.Base import Base

class Serial(Base):
    def __init__(self, endpoint):
        self.__endpoint = endpoint
        self.__message_buffer = ''
        self.__serial = None

    def connect(self):
        self.__serial = serial.Serial(self.__endpoint['port'], self.__endpoint['baud_rate'], timeout=0.5)

    def disconnect(self):
        self.__serial.close()

    def send(self, which, value):
        self.__serial.write(which.encode('ascii'))
        self.__serial.write(':'.encode('ascii'))
        self.__serial.write(value)

    def listen(self, complete_message_callback, receive_message_callback):
        received_data = self.__serial.read().decode('utf-8')
        if received_data == False or received_data == '':
            return
        self.get_logger().debug("Senzors data received from serial: {0}".format(received_data))
        self.__message_buffer += received_data
        if not complete_message_callback(self.__message_buffer):
            return
        receive_message_callback(self.__message_buffer)
        self.__message_buffer = ''

    def __get_endpoint(self):
        return self.__endpoint