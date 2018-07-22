import numpy


class ModelCleanup:
    def __init__(self, mean_rain_threshold: float, exclude_fields_from_prediction: list, predicted_variable: str) -> None:
        self.__mean_rain_threshold = mean_rain_threshold
        self.__exclude_fields_from_prediction = exclude_fields_from_prediction
        self.__predicted_variable = predicted_variable

    def get_cleanned(self, dataframe):
        dataframe = dataframe.set_index('date', False)
        dataframe.insert(loc=1, column='has_rain',
                         value=numpy.where(dataframe[self.__predicted_variable] > self.__mean_rain_threshold, 1, 0))
        dataframe = dataframe.drop(self.__exclude_fields_from_prediction, axis=1, errors='ignore')
        for exclusion in self.__exclude_fields_from_prediction:
            dataframe.filter(like=exclusion, axis=1)
        # dataframe = dataframe.filter(self.__exclude_fields_from_prediction, axis=1, errors='ignore')

        return dataframe[dataframe['temperature_outside_mean'] >= 0]