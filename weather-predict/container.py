from typing import Callable

from pymongo import MongoClient

import config
from keras_wrapper.KerasModelBuilder import KerasModelBuilder
from keras_wrapper.KerasGridSearch import KerasGridSearch
from repository.DatapointsRepository import DatapointsRepository
from data_source.FinalDataProvider import FinalDataProvider
from model.Sensors import Sensors
from model.DataFeatures import DataFeatures


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
        return DatapointsRepository(self.mongo_client())

    @singleton
    def final_data_provider(self) -> FinalDataProvider:
        return FinalDataProvider(self.datapoints_repository(), Sensors.list(), DataFeatures.list())