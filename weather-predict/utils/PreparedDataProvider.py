from datetime import datetime, timedelta

import pandas
import numpy

from data_processing.AggregateEnrichProcessor import AggregateEnrichProcessor
from data_processing.HistoryDatapointAugmenterProcessor import HistoryDatapointAugmenterProcessor
from data_processing.CleanupProcessor import CleanupProcessor
from repository.DatapointsRepository import DatapointsRepository
from utils.SensorTypeDatasourceMap import SensorTypeDatasourceMap


class PreparedDataProvider:
    MINIMUM_RAIN_TRHRESHOLD = 0.000

    def __init__(self, datapoits_repository: DatapointsRepository, sensor_type_datasource_map: SensorTypeDatasourceMap,
                 datafeatures) -> None:
        self.__datapoints_repository = datapoits_repository
        self.__sensor_type_datasource_map = sensor_type_datasource_map
        self.__datafeatures = datafeatures

    def get(self, days_behind: int, datapoints_behind: int, hour_granularity: int, data_source: str):
        sensor_types = self.__sensor_type_datasource_map.get(data_source)
        hour_group_stats = AggregateEnrichProcessor(hour_granularity, sensor_types)
        cleanup_processor = CleanupProcessor(sensor_types, self.__datafeatures)
        datapoint_augmenter_processor = HistoryDatapointAugmenterProcessor(datapoints_behind)
        extracted_data = []

        for day_behind in range(days_behind, 0, -5):
            start_date = datetime.today() - timedelta(days=day_behind)
            end_date = datetime.today() - timedelta(days=(day_behind - 5))
            datapoints = self.__datapoints_repository.get(data_source, start_date, end_date)
            extracted_data += datapoints

        dataframe = pandas.DataFrame(extracted_data).set_index('_id')
        dataframe = dataframe.dropna()
        dataframe = hour_group_stats.process(dataframe)
        dataframe.insert(loc=1, column='has_rain',
                         value=numpy.where(dataframe['rain_max'] > self.MINIMUM_RAIN_TRHRESHOLD, 1, 0))
        dataframe = dataframe.drop(['date'], axis=1)
        dataframe.loc['last'] = [0 for n in range(len(dataframe.columns))]
        dataframe = datapoint_augmenter_processor.process(dataframe)
        dataframe = dataframe.iloc[datapoints_behind:]

        return cleanup_processor.process(dataframe)
