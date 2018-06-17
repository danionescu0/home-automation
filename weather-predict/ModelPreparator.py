import numpy

import config


class ModelPreparator:
    def prepare(self, dataframe):
        dataframe = dataframe.set_index('date')
        dataframe['has_rain'] = numpy.where(dataframe['rain_outside_mean'] > 5, 1, 0)
        dataframe = dataframe.drop(['rain_outside_mean', 'rain_outside_min'], axis=1)
        dataframe = dataframe[dataframe['temperature_outside_mean'] >= 0]
        for feature in dataframe.dtypes.index:
            if feature == 'date':
                continue
            for datapoint_nr_behind in range(1, 4):
                self.__derive_nth_datapoint_feature(dataframe, feature, datapoint_nr_behind)

        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])

        return self.__exclude_current_predictions(dataframe)

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
                if full_name in ['rain_outside_mean', 'rain_outside_min']:
                    continue
                to_exclude.append(full_name)
        print(to_exclude)
        dataframe.drop(to_exclude, axis=1)

        return dataframe