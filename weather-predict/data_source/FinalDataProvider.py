from datetime import datetime, timedelta

import pandas
import numpy

from data_processing.HourGroupStatsProcessor import HourGroupStatsProcessor
from data_processing.CleanupProcessor import CleanupProcessor
from data_processing.DatapointAugmenterProcessor import DatapointAugmenterProcessor
from data_processing.RemoveCurrentProcessor import RemoveCurrentProcessor
from repository.DatapointsRepository import DatapointsRepository


class FinalDataProvider:
    MINIMUM_RAIN_TRHRESHOLD = 0.1

    def __init__(self, datapoits_repository: DatapointsRepository, sensors: list, datafeatures) -> None:
        self.__datapoints_repository = datapoits_repository
        self.__sensors = sensors
        self.__datafeatures = datafeatures

    def get(self, days_behind: int, datapoints_behind: int, hour_granularity: int):
        hour_group_stats = HourGroupStatsProcessor(hour_granularity, self.__sensors)
        cleanup_processor = CleanupProcessor()
        remove_current_processor = RemoveCurrentProcessor(self.__sensors, self.__datafeatures)
        datapoint_augmenter_processor = DatapointAugmenterProcessor(datapoints_behind)
        extracted_data = []

        for day_behind in range(days_behind, 0, -5):
            start_date = datetime.today() - timedelta(days=day_behind)
            end_date = datetime.today() - timedelta(days=(day_behind - 5))
            datapoints = self.__datapoints_repository.get(start_date, end_date)
            extracted_data += datapoints

        dataframe = pandas.DataFrame(extracted_data).set_index('_id')
        dataframe = dataframe.dropna()
        dataframe = hour_group_stats.process(dataframe)
        dataframe.insert(loc=1, column='has_rain',
                         value=numpy.where(dataframe['rain_avg'] > self.MINIMUM_RAIN_TRHRESHOLD, 1, 0))
        dataframe = cleanup_processor.process(dataframe)
        dataframe = datapoint_augmenter_processor.process(dataframe)
        dataframe = dataframe.iloc[datapoints_behind:]

        return remove_current_processor.process(dataframe)
