from data_processing.BaseProcessor import BaseProcessor


class CleanupProcessor(BaseProcessor):
    def __init__(self, sensor_names: list, feature_names: list) -> None:
        self.__sensor_names = sensor_names
        self.__feature_names = feature_names

    def process(self, dataframe):
        cols = [col_name for col_name in dataframe.columns if 'rain' not in col_name or col_name == 'has_rain']
        dataframe = dataframe[cols]
        to_remove = [sensor + '_' + feature for sensor in self.__sensor_names for feature in self.__feature_names]

        return dataframe.drop(to_remove, axis=1, errors='ignore')