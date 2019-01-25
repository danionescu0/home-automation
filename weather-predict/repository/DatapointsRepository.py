from typing import List

from pymongo import MongoClient

from model.Sensor import Sensor
from utils.SensorTypeDatasourceMap import SensorTypeDatasourceMap


class DatapointsRepository:
    def __init__(self, mongo_client: MongoClient, sensor_type_datasource_map: SensorTypeDatasourceMap) -> None:
        self.__mongo_client = mongo_client
        self.__sensor_type_datasource_map = sensor_type_datasource_map

    def update(self, datasource: str, date, sensors: List[Sensor]):
        set_data = {sensor.type: sensor.value for sensor in sensors}
        set_data['date'] = date
        self.__get_client(datasource).update(
            {'_id': date.strftime('%m_%d_%Y_%H_%M')},
            {'$set': set_data},
            upsert=True
        )

    def get(self, datasource: str, start_date, end_date) -> list:
        cursor = self.__get_client(datasource).find(
            {'$and': [
                {'date': {'$gte': start_date}},
                {'date': {'$lte': end_date}}
            ]}
        )
        sensor_types = self.__sensor_type_datasource_map.get(datasource)

        return list(filter(
            lambda dp: True if all(sensor_type in dp for sensor_type in sensor_types) else False, cursor)
        )

    def __get_client(self, datasource: str):
        return self.__mongo_client['weather'][datasource]