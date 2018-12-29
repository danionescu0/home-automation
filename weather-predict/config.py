# replace url with your own ip or url
url = "http://danionescu0.go.ro:8080/api/sensor/{0}?start_date={1}&end_date={2}"

# replace sensors names with your own
home_automation_sensor_mapping = {
    'humidity_outside' : 'humidity',
    'airPressure_outside' : 'pressure',
    'temperature_outside' : 'temperature',
    'rain_outside': 'rain',
    'light_outside': 'light'
}

mongodb = {
    'host' : 'localhost',
    'port' : 27017
}

model = {
    'keras_model_file_name' : 'weather.h5',
    'sklearn_scaler_file_name' : 'scaler.save'
}