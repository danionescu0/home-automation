from data_processing.BaseProcessor import BaseProcessor


# For a given dataframe, add rows as column:
# Ex: X  Y  Z
#     1  2  1
#     5  6  9
#     2  3  3
# Given 1 datapoint behind transformed to:
# Ex: X  Y  Z X_1 Y_1 Z_1
#     5  6  9 1   2   1
#     2  3  3 5   6   9
class DatapointAugmenterProcessor(BaseProcessor):
    ID_COLUMN = '_id'

    def __init__(self, datapoints_behind: int) -> None:
        self.__datapoints_behind = datapoints_behind

    def process(self, dataframe):
        for feature in dataframe.dtypes.index:
            if feature == self.ID_COLUMN:
                continue
            for datapoint_nr_behind in range(1, self.__datapoints_behind + 1):
                self.__derive_nth_datapoint_feature(dataframe, feature, datapoint_nr_behind)

        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])

        return dataframe

    def __derive_nth_datapoint_feature(self, dataframe, feature, datapoint_nr_behind):
        rows = dataframe.shape[0]
        nth_prior_measurements = [None] * datapoint_nr_behind + \
                                 [dataframe[feature][i - datapoint_nr_behind] for i in range(datapoint_nr_behind, rows)]
        col_name = "{}_{}".format(feature, datapoint_nr_behind)
        dataframe[col_name] = nth_prior_measurements