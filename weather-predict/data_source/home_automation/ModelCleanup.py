import numpy


class ModelCleanup:
    def __init__(self, mean_rain_threshold: float) -> None:
        self.__mean_rain_threshold = mean_rain_threshold

    def get_cleanned(self, dataframe):
        dataframe = dataframe.set_index('date', False)
        dataframe['has_rain'] = numpy.where(dataframe['rain_outside_mean'] > self.__mean_rain_threshold, 1, 0)
        dataframe = dataframe.drop(['rain_outside_mean', 'rain_outside_min', 'rain_outside_max'], axis=1)

        return dataframe[dataframe['temperature_outside_mean'] >= 0]