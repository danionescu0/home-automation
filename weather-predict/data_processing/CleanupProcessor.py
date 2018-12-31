from data_processing.BaseProcessor import BaseProcessor


class CleanupProcessor(BaseProcessor):
    MINIMUM_MEDIAN_TEMPERATURE = 0

    def process(self, dataframe):
        dataframe = dataframe.drop(['date'], axis=1, errors='ignore')

        return dataframe[dataframe['temperature_avg'] >= self.MINIMUM_MEDIAN_TEMPERATURE]