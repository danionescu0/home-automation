from data_processing.BaseProcessor import BaseProcessor


class CleanupProcessor(BaseProcessor):
    MINIMUM_MEDIAN_TEMPERATURE = 0

    def process(self, dataframe):
        dataframe = dataframe.drop(['date'], axis=1)

        return dataframe[dataframe['temperature_min'] >= self.MINIMUM_MEDIAN_TEMPERATURE]