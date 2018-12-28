from typing import List

from pymongo import MongoClient

from model.Datapoint import Datapoint


class DatapointsRepository:
    def __init__(self, mongo_client: MongoClient) -> None:
        self.__mongo_client = mongo_client

    def add(self, datapoint: Datapoint):
        pass

    def update(self, date, sensor_name: str, value: float):
        self.__mongo_client.update(
            {'_id' : date.strftime('%m_%d_%Y_%H_%M')},
            {'$set' : {sensor_name : value, 'date' : date}},
            upsert=True
        )

    def get(self, start_date, end_date) -> List[Datapoint]:
        cursor = self.__mongo_client.find(
            {'$and' : [
                {'date' : {'$gte' : start_date}},
                {'date' : {'$lte' : end_date}}
            ]}
        )

        return list(cursor)