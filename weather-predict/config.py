# replace url with your own ip or url
url = "http://danionescu0.go.ro:8080/api/sensor/{0}?start_date={1}&end_date={2}"

# replace sensors names with your own
sensors = ['humidity_outside', 'airPressure_outside', 'temperature_outside', 'rain_outside', 'light_outside']

# exclude fields that influence the variable you try to predict, or useless fields
exclude_fields_from_prediction = ['rain_outside_mean', 'rain_outside_min', 'rain_outside_max',
                                  'rain_outside_raise', 'rain_outside_fall', 'rain_outside_stdev', 'hour_group']

mongodb = {
    'host' : 'localhost',
    'port' : 27017
}

model = {
    'keras_model_file_name' : 'weather.h5',
    'sklearn_scaler_file_name' : 'scaler.save'
}