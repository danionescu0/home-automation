import json

from Crypto.Cipher import AES

from Serial import Serial


class SerialAESDevice:
    DELIMITER = ':'

    def __init__(self, aes_key: str, serial: Serial, mqtt_serial_integration: dict) -> None:
        self.__aes_key = aes_key
        self.__serial = serial
        self.__mqtt_serial_integration = mqtt_serial_integration
        self.__first_call = True

    def incomming_message(self, message: bytes):
        if self.__first_call == True:
            self.__first_call = False
            return
        data = json.loads(message.decode())
        id = data['id']
        state = data['state']
        if id not in self.__mqtt_serial_integration:
            return
        send_message = self.__mqtt_serial_integration[id][state]
        if len(send_message) > 16:
            raise RuntimeError("Aes encription does not handle more than 16 characters")
        padded_text = send_message.ljust(16, ' ')
        aes = AES.new(self.__aes_key, AES.MODE_CBC, IV=self.__aes_key)
        encripted = aes.encrypt(padded_text.encode())
        self.__serial.send(self.__mqtt_serial_integration[id]['device'].encode('ascii'))
        self.__serial.send(self.DELIMITER.encode('ascii'))
        self.__serial.send(encripted)
        print(message)
        print(data)
        print(send_message)
        print(encripted)