serial = {
    'port': '/dev/ttyACM0',
    'baud_rate': '9600',
    'aes_key': '0000000000000000'
}

mqtt = {
    'host': '192.168.1.33'
}

weather_station_mappings = {
    'T1': 'temperature',
    'H1': 'humidity',
    'PS1': 'pressure',
    'V1': 'voltage',
    'R1': 'rain',
}

mqtt_serial_integration = {
    'balcony_courtains': {
        'device': 'L2',
        'on': 'C20|',
        'off': 'O30|'
    }
}