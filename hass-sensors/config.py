weather_station_mappings = {
    'T1': {
        'discovery_topic': 'homeassistant/sensor/outside_humidity/config',
        'discovery_message': '{"name": "outside_humidity", "device_class": "humidity", "state_topic": "homeassistant/sensor/outside_humidity/state"}',
        'state_topic': 'homeassistant/sensor/outside_humidity/state'
    },
    # 'H1': 'humidity',
    # 'PS1': 'pressure',
    # 'V1': 'voltage',
    # 'R1': 'rain',
}