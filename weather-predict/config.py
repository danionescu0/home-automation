# replace url with your own ip or url
url = "http://danionescu0.go.ro:8080/api/sensor/{0}?start_date={1}&end_date={2}"

# replace sensors names with your own
sensors = ['humidity_outside', 'airPressure_outside', 'temperature_outside', 'rain_outside', 'light_outside']

# data in a day can be splitted into some number of hours batches
grouped_by_hours = 12