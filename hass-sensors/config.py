weather_station_mappings = {
    'T1': {
        'discovery_topic': 'homeassistant/sensor/outside_temperature/config',
        'discovery_message': '{"name": "outside_temperature", "device_class": "temperature", "state_topic": "homeassistant/sensor/outside_temperature/state"}',
        'state_topic': 'homeassistant/sensor/outside_temperature/state'
    },
    'H1': {
        'discovery_topic': 'homeassistant/sensor/outside_humidity/config',
        'discovery_message': '{"name": "outside_humidity", "device_class": "humidity", "state_topic": "homeassistant/sensor/outside_humidity/state"}',
        'state_topic': 'homeassistant/sensor/outside_humidity/state'
    },
    'PS1': {
        'discovery_topic': 'homeassistant/sensor/outside_pressure/config',
        'discovery_message': '{"name": "outside_pressure", "device_class": "pressure", "state_topic": "homeassistant/sensor/outside_pressure/state"}',
        'state_topic': 'homeassistant/sensor/outside_pressure/state'
    },
    'V1': {
        'discovery_topic': 'homeassistant/sensor/outside_voltage/config',
        'discovery_message': '{"name": "outside_voltage", "device_class": "voltage", "state_topic": "homeassistant/sensor/outside_voltage/state"}',
        'state_topic': 'homeassistant/sensor/outside_voltage/state'
    },
    'R1': {
        'discovery_topic': 'homeassistant/sensor/outside_rain/config',
        'discovery_message': '{"name": "outside_rain", "device_class": "power_factor", "state_topic": "homeassistant/sensor/outside_rain/state"}',
        'state_topic': 'homeassistant/sensor/outside_rain/state'
    },
    'L1': {
        'discovery_topic': 'homeassistant/sensor/outside_light/config',
        'discovery_message': '{"name": "outside_light", "device_class": "illuminance", "state_topic": "homeassistant/sensor/outside_light/state"}',
        'state_topic': 'homeassistant/sensor/outside_light/state'
    }
}