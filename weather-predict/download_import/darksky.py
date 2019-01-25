import argparse
from datetime import datetime, timedelta

import requests

import config
from model.Sensor import Sensor
from container import Container
from model.DataSource import DataSource


argparse = argparse.ArgumentParser()
argparse.add_argument("-d", "--days-behind", required=True, dest="days_behind", type=int, help="Days behind")
args = vars(argparse.parse_args())

container = Container()
datapoint_repository = container.datapoints_repository()
start_date = datetime.today() - timedelta(days=args['days_behind'])

for day_behind in range(args['days_behind'], 0, -1):
    start_date = datetime.today() - timedelta(days=day_behind)
    print('Calculating for date: ' + start_date.strftime('%m-%d-%Y'))
    request_url = config.darksky_url.format(int(start_date.timestamp()))
    response = requests.get(request_url)
    try:
        sensors_data = response.json()['hourly']['data']
    except Exception:
        print("Error transforming to json")
        continue
    for sensor_data in sensors_data:
        for darksky_sensor_name, sensor_name in config.darksky_sensor_mapping.items():
            if darksky_sensor_name not in sensor_data:
                continue
            date = datetime.fromtimestamp(sensor_data['time'])
            sensor = Sensor(sensor_name, float(sensor_data[darksky_sensor_name]))
            datapoint_repository.update(DataSource.DARKSKY.value, date, [sensor])