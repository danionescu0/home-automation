import argparse
from datetime import datetime, timedelta

import requests
from pymongo import MongoClient

import config
from repository.DatapointsRepository import DatapointsRepository


argparse = argparse.ArgumentParser()
argparse.add_argument("-d", "--day-behind", required=True, dest="days_behind", type=int, help="Days behind")
args = vars(argparse.parse_args())


mongo_client = MongoClient(config.mongodb['host'], config.mongodb['port']).weather.datapoints
datapoint_repository = DatapointsRepository(mongo_client)
start_date = datetime.today() - timedelta(days=args['days_behind'])

for day_behind in range(args['days_behind'], 0, -1):
    start_date = datetime.today() - timedelta(days=day_behind)
    print('Calculating for date: ' + start_date.strftime('%m-%d-%Y'))

    for home_automation_sensor_name, sensor_name in config.home_automation_sensor_mapping.items():
        literal_date = start_date.strftime('%m-%d-%Y')
        request = config.url.format(home_automation_sensor_name, literal_date, literal_date)
        response = requests.get(request)
        sensors_data = response.json()['data']
        if not len(sensors_data) or len(sensors_data) < 130:
            continue
        for sensor_data in sensors_data:
            date = datetime.fromtimestamp(sensor_data['timestamp'])
            datapoint_repository.update(date, sensor_name, float(sensor_data['value']))