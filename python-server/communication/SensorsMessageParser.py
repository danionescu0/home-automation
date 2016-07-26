class SensorsMessageParser:
    def __init__(self):
        self.__sensor_separator = '|'

    def is_buffer_parsable(self, buffer):
        return buffer.endswith(self.__sensor_separator)

    def parse_sensors_string(self, text_buffer):
        text_buffer = text_buffer[:-1]
        sensors = {}
        for sensor in text_buffer.split('|'):
            elements = sensor.split(':')
            if elements[0] == 'H':
                sensors['humidity'] = int(elements[1])
            if elements[0] == 'T':
                sensors['temperature'] = int(elements[1])
            if elements[0] == 'L':
                sensors['light'] = int(elements[1])
            if elements[0] == 'R':
                sensors['rain'] = int(elements[1])
            if elements[0] == 'P':
                sensors['presence'] = int(elements[1])
            if elements[0] == 'Q':
                sensors['airQuality'] = int(elements[1])
            if elements[0] == 'F':
                sensors['fingerprint'] = int(elements[1])

        return sensors