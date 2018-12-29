from data_processing.BaseProcessor import BaseProcessor


class CleanupProcessor(BaseProcessor):
    MINIMUM_MEDIAN_TEMPERATURE = 'temperature_avg'

    def process(self, dataframe):
        dataframe = dataframe.drop(['date'], axis=1, errors='ignore')

        return dataframe[dataframe[self.MINIMUM_MEDIAN_TEMPERATURE] >= 0]