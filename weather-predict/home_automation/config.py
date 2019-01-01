# replace url with your own ip or url
url = "http://host/api/sensor/{0}?start_date={1}&end_date={2}"

# replace sensors names with your own
home_automation_sensor_mapping = {
    'humidity_outside': 'humidity',
    'airPressure_outside': 'pressure',
    'temperature_outside': 'temperature',
    'rain_outside': 'rain',
    'light_outside': 'light'
}

#same as main config
mongodb = {
    'host': 'localhost',
    'port': 27017
}