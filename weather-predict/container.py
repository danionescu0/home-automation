from typing import Callable

from pymongo import MongoClient

import config
from keras_wrapper.KerasModelBuilder import KerasModelBuilder
from keras_wrapper.KerasGridSearch import KerasGridSearch
from repository.DatapointsRepository import DatapointsRepository
from utils.PreparedDataProvider import PreparedDataProvider
from model.DataFeatures import DataFeatures
from device_communication.Serial import Serial
from device_communication.SensorBuilder import SensorBuilder
from utils.EmailNotifier import EmailNotifier
from utils.SensorTypeDatasourceMap import SensorTypeDatasourceMap


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
        return MongoClient(config.mongodb['host'], config.mongodb['port'])

    @singleton
    def datapoints_repository(self) -> DatapointsRepository:
        return DatapointsRepository(self.mongo_client(), self.sensor_type_datasource_map())

    @singleton
    def prepared_data_provider(self) -> PreparedDataProvider:
        return PreparedDataProvider(self.datapoints_repository(), self.sensor_type_datasource_map(), DataFeatures.list())

    @singleton
    def serial(self) -> Serial:
        return Serial(config.serial['port'], config.serial['baud_rate'])

    @singleton
    def sensor_builder(self) -> SensorBuilder:
        return SensorBuilder()

    @singleton
    def email_notifier(self) -> EmailNotifier:
        return EmailNotifier()

    @singleton
    def sensor_type_datasource_map(self) -> SensorTypeDatasourceMap:
        return SensorTypeDatasourceMap()