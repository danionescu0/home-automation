def parseSensorsString(data):
    sensors = {}
    for sensor in data.split('|'):
        elements = sensor.split(':')
        if elements[0] == 'H':
            sensors['humidity'] = elements[1]
        if elements[0] == 'T':
            sensors['temperature'] = elements[1]
        if elements[0] == 'L':
            sensors['light'] = elements[1]

    return sensors