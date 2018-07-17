import config


# For a given dataframe, add rows as column:
# Ex: X  Y  Z
#     1  2  1
#     5  6  9
#     2  3  3
# Given 1 datapoint behind transformed to:
# Ex: X  Y  Z X_1 Y_1 Z_1
#     5  6  9 1   2   1
#     2  3  3 5   6   9
class DatapointAugmenter:
    def prepare(self, dataframe, datapoints_behind: int, date_column: str):
        dataframe = dataframe.set_index(date_column)
        for feature in dataframe.dtypes.index:
            if feature == date_column:
                continue
            for datapoint_nr_behind in range(1, datapoints_behind + 1):
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
                if full_name in ['rain_outside_mean', 'rain_outside_min', 'rain_outside_max']:
                    continue
                to_exclude.append(full_name)

        return dataframe.drop(to_exclude, axis=1)