class ModelPreparator:
    def prepare(self, dataframe):
        dataframe = dataframe.set_index('date')
        # dataframe['has_rain'] = numpy.where(dataframe['rain_outside_mean'] > 0, 1, 0)
        dataframe = dataframe.drop(['rain_outside_mean', 'rain_outside_min'], axis=1)
        dataframe = dataframe[dataframe['temperature_outside_min'] >= 0]
        for feature in dataframe.dtypes.index:
            if feature == 'date':
                continue
            for N in range(1, 4):
                self.__derive_nth_day_feature(dataframe, feature, N)

        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])
        dataframe = dataframe.drop(dataframe.index[[0]])

        return dataframe

    def __derive_nth_day_feature(self, dataframe, feature, N):
        rows = dataframe.shape[0]
        nth_prior_measurements = [None] * N + [dataframe[feature][i - N] for i in range(N, rows)]
        col_name = "{}_{}".format(feature, N)
        dataframe[col_name] = nth_prior_measurements