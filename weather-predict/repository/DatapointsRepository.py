from typing import List

from pymongo import MongoClient

from model.Sensor import Sensor


class DatapointsRepository:
    def __init__(self, mongo_client: MongoClient, sensor_types: list) -> None:
        self.__mongo_client = mongo_client
        self.__sensor_types = sensor_types

    def update(self, date, sensors: List[Sensor]):
        set_data = {sensor.type : sensor.value for sensor in sensors}
        set_data['date'] = date
        self.__mongo_client.update(
            {'_id' : date.strftime('%m_%d_%Y_%H_%M')},
            {'$set' : set_data},
            upsert=True
        )

    def get(self, start_date, end_date) -> list:
        cursor = self.__mongo_client.find(
            {'$and' : [
                {'date' : {'$gte' : start_date}},
                {'date' : {'$lte' : end_date}}
            ]}
        )

        return list(filter(
            lambda dp: True if all(sensor_type in dp for sensor_type in self.__sensor_types) else False, cursor)
        )