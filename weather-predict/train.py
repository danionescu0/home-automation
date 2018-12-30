import argparse

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

import config
from utils import print_headline
from container import Container


argparse = argparse.ArgumentParser()
argparse.add_argument("-d", "--days-behind", required=True, dest="days_behind", type=int,
                      help="Days behind to be taken into account")
argparse.add_argument("-p", "--test-file-percent", required=True, dest="test_file_percent", type=int,
                      help="Percent of the data that will be generated into a separate test file")
argparse.add_argument("-dp", "--datapoints-behind", required=True, dest="datapoints_behind", type=int,
                      help="Datapoints behind to be added for the model on each line")
argparse.add_argument("-hg", "--hour-granularity", required=True, dest="hour_granularity", type=int,
                      help="How many hours a datapoint will agregate")
argparse.add_argument('--grid-search', dest='grid_search', action='store_true')
args = vars(argparse.parse_args())

container = Container()
dataframe = container.final_data_provider().get(args['days_behind'], args['datapoints_behind'], args['hour_granularity'])
main_data, test_data = train_test_split(dataframe, test_size=args['test_file_percent'] / 100)

main_data.to_csv('sample_data/main_data.csv')
test_data.to_csv('sample_data/test_data.csv')

print_headline('Training neural net')


X = main_data.iloc[:, 1:].values
y = main_data.iloc[:, 0].values
scaler = StandardScaler()
X = scaler.fit_transform(X)

if args['grid_search']:
    print(container.keras_grid_search().search(X, y))

model_builder = container.keras_model_builder()
classifier = model_builder.build(X.shape[1], 'rmsprop', 0.05)
classifier.fit(X, y, batch_size=1, epochs=50)

classifier.save(config.model['keras_model_file_name'])
joblib.dump(scaler, config.model['sklearn_scaler_file_name'])