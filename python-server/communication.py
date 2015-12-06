class communication:
    def __init__(self):
        self.__btSeparator = '|'

    def isBufferParsable(self, buffer):
        return buffer.endswith(self.__btSeparator)

    def parseSensorsString(self, btBuffer):
        btBuffer = btBuffer[:-1]

        sensors = {}
        for sensor in btBuffer.split('|'):
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

        return sensors