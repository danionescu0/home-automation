from typing import Callable

from pymongo import MongoClient

import config
from keras_wrapper.KerasModelBuilder import KerasModelBuilder
from keras_wrapper.KerasGridSearch import KerasGridSearch
from repository.DatapointsRepository import DatapointsRepository
from data_source.FinalDataProvider import FinalDataProvider
from model.SensorTypes import SensorTypes
from model.DataFeatures import DataFeatures
from device_communication.Serial import Serial
from device_communication.SensorBuilder import SensorBuilder
from utils.EmailNotifier import EmailNotifier


def singleton(function: Callable):
    caching = {}
    def wrapper(*args, **kwargs):
        if function.__name__ in caching:
            return caching[function.__name__]
        caching[function.__name__] = function(*args, **kwargs)

        return caching[function.__name__]

    return wrapper


class Container:
    @singleton
    def keras_model_builder(self) -> KerasModelBuilder:
        return KerasModelBuilder()

    @singleton
    def keras_grid_search(self) -> KerasGridSearch:
        return KerasGridSearch(self.keras_model_builder())

    @singleton
    def mongo_client(self) -> MongoClient:
        return MongoClient(config.mongodb['host'], config.mongodb['port']).weather.datapoints

    @singleton
    def datapoints_repository(self) -> DatapointsRepository:
        return DatapointsRepository(self.mongo_client(), SensorTypes.list())

    @singleton
    def final_data_provider(self) -> FinalDataProvider:
        return FinalDataProvider(self.datapoints_repository(), SensorTypes.list(), DataFeatures.list())

    @singleton
    def serial(self) -> Serial:
        return Serial(config.serial['port'], config.serial['baud_rate'])

    @singleton
    def sensor_builder(self) -> SensorBuilder:
        return SensorBuilder()

    @singleton
    def email_notifier(self) -> EmailNotifier:
        return EmailNotifier()