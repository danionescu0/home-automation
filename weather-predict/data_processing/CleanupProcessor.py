import numpy

from data_processing.BaseProcessor import BaseProcessor


class CleanupProcessor(BaseProcessor):
    PREDICTED_VARIABLE = 'rain_avg'
    MINIMUM_MEDIAN_TEMPERATURE = 'temperature_avg'

    def __init__(self, mean_rain_threshold: float) -> None:
        self.__mean_rain_threshold = mean_rain_threshold

    def process(self, dataframe):
        dataframe.insert(loc=1, column='has_rain',
                         value=numpy.where(dataframe[self.PREDICTED_VARIABLE] > self.__mean_rain_threshold, 1, 0))
        dataframe = dataframe.drop(['date'], axis=1, errors='ignore')

        return dataframe[dataframe[self.MINIMUM_MEDIAN_TEMPERATURE] >= 0]