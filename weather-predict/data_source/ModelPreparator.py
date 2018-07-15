import numpy

import config


class ModelPreparator:
    def __init__(self, mean_rain_threshold = 0.5) -> None:
        self.__mean_rain_threshold = mean_rain_threshold

    def prepare(self, dataframe, days_behind: int):
        dataframe = dataframe.set_index('date')
        dataframe['has_rain'] = numpy.where(dataframe['rain_outside_mean'] > self.__mean_rain_threshold, 1, 0)
        dataframe = dataframe.drop(['rain_outside_mean', 'rain_outside_min', 'rain_outside_max'], axis=1)
        dataframe = dataframe[dataframe['temperature_outside_mean'] >= 0]
        for feature in dataframe.dtypes.index:
            if feature == 'date':
                continue
            for datapoint_nr_behind in range(1, days_behind + 1):
                self.__derive_nth_datapoint_feature(dataframe, feature, datapoint_nr_behind)

        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = self.__exclude_current_predictions(dataframe)

        input_data = dataframe[[col for col in dataframe.columns if col != 'has_rain']]
        output_data = dataframe['has_rain']

        return dataframe, input_data, output_data

    def __derive_nth_datapoint_feature(self, dataframe, feature, datapoint_nr_behind):
        rows = dataframe.shape[0]
        nth_prior_measurements = [None] * datapoint_nr_behind + \
                                 [dataframe[feature][i - datapoint_nr_behind] for i in range(datapoint_nr_behind, rows)]
        col_name = "{}_{}".format(feature, datapoint_nr_behind)
        dataframe[col_name] = nth_prior_measurements

    def __exclude_current_predictions(self, dataframe):
        to_exclude = []
        for sensor in config.sensors:
            for suffix in ['min', 'max', 'mean']:
                full_name = '{0}_{1}'.format(sensor, suffix)
                if full_name in ['rain_outside_mean', 'rain_outside_min', 'rain_outside_max']:
                    continue
                to_exclude.append(full_name)

        return dataframe.drop(to_exclude, axis=1)