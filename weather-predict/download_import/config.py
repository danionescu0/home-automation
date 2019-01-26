#same as main config
mongodb = {
    'host': 'localhost',
    'port': 27017
}

# home automation import
#######################

# replace url with your own ip or url
url = "http://your_host/api/sensor/{0}?start_date={1}&end_date={2}"

# replace sensors names with your own
home_automation_sensor_mapping = {
    'humidity_outside': 'humidity',
    'airPressure_outside': 'pressure',
    'temperature_outside': 'temperature',
    'rain_outside': 'rain',
    'light_outside': 'light'
}

# dark sky import
#################

# url conaining the api key, latitude and longitude
darksky_url = "https://api.darksky.net/forecast/your_api_key/44.4205455,26.1496616,{0}"

darksky_sensor_mapping = {
    'humidity': 'humidity',
    'pressure': 'pressure',
    'temperature': 'temperature',
    'uvIndex': 'uv_index',
    'precipIntensity': 'rain',
    'dewPoint': 'dewpoint',
    'windSpeed': 'wind_speed',
    'windGust': 'wind_gust',
    'windBearing': 'wind_bearing',
    'cloudCover': 'cloud_cover',
    'visibility': 'visibility'
}