import pprint
import argparse
from datetime import datetime, timedelta

import pandas
from sklearn.model_selection import train_test_split
from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

import config
from keras_wrapper.ModelBuilder import ModelBuilder
from keras_wrapper.GridSearch import GridSearch
from repository.DatapointsRepository import DatapointsRepository
from data_processing.HourGroupStatsProcessor import HourGroupStatsProcessor
from data_processing.CleanupProcessor import CleanupProcessor
from data_processing.DatapointAugmenterProcessor import DatapointAugmenterProcessor

argparse = argparse.ArgumentParser()
argparse.add_argument("-d", "--day-behind", required=True, dest="days_behind", type=int,
                      help="Days behind to be taken into account")
argparse.add_argument("-p", "--test-file-percent", required=True, dest="test_file_percent", type=int,
                      help="Percent of the data that will be generated into a separate test file")
argparse.add_argument("-dp", "--datapoints-behind", required=True, dest="datapoints_behind", type=int,
                      help="Datapoints behind to be added for the model on each line")
argparse.add_argument("-hg", "--hour-granularity", required=True, dest="hour_granularity", type=int,
                      help="How many hours a datapoint will agregate")
args = vars(argparse.parse_args())


mongo_client = MongoClient(config.mongodb['host'], config.mongodb['port']).weather.datapoints
datapoint_repository = DatapointsRepository(mongo_client)
hour_group_stats = HourGroupStatsProcessor(args['hour_granularity'])
cleanup_processor = CleanupProcessor(0.1)
datapoint_augmenter_processor = DatapointAugmenterProcessor(args['datapoints_behind'])

from_date = to_date = start_date = datetime.today() - timedelta(days=args['days_behind'])
end_date = datetime.today()
extracted_data = []

print('Getting data from the database')
for day_behind in range(args['days_behind'], 0, -1):
    start_date = datetime.today() - timedelta(days=day_behind)
    end_date = datetime.today() - timedelta(days=(day_behind - 1))
    datapoints = datapoint_repository.get(start_date, end_date)
    extracted_data += datapoints

print('Applying processing')

dataframe = pandas.DataFrame(extracted_data).set_index('_id')
dataframe = hour_group_stats.process(dataframe)
dataframe = cleanup_processor.process(dataframe)
dataframe = datapoint_augmenter_processor.process(dataframe)
dataframe = dataframe.iloc[args['datapoints_behind']:]
dataframe = dataframe.dropna()
dataframe = dataframe.drop(
    ['rain_avg', 'rain_fall', 'rain_rise', 'rain_min', 'rain_max',
     'temperature_avg', 'temperature_fall', 'temperature_rise', 'temperature_min', 'temperature_max',
     'humidity_avg', 'humidity_fall', 'humidity_rise', 'humidity_min', 'humidity_max',
     'pressure_avg', 'pressure_fall', 'pressure_rise', 'pressure_min', 'pressure_max',
     'light_avg', 'light_fall', 'light_rise', 'light_min', 'light_max'],
    axis=1)
pprint.pprint(dataframe.head())
print(dataframe.describe().T)

main_data, test_data = train_test_split(dataframe, test_size=args['test_file_percent'] / 100)

dataframe.to_csv('sample_data/all_data.csv')
main_data.to_csv('sample_data/main_data.csv')
test_data.to_csv('sample_data/test_data.csv')

print('Training neural net')

model_builder = ModelBuilder()
grid_search = GridSearch(model_builder)
scaler = StandardScaler()

X = main_data.iloc[:, 1:].values
y = main_data.iloc[:, 0].values

X = scaler.fit_transform(X)
joblib.dump(scaler, config.model['sklearn_scaler_file_name'])

# if args['mode'] == 'grid':
#     print(grid_search.search(X, y))
#     sys.exit()

classifier = model_builder.build(X.shape[1], 'adam', 0.1)
classifier.fit(X, y, batch_size=1, nb_epoch=7)
classifier.save(config.model['keras_model_file_name'])