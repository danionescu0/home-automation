import argparse
import math

import numpy as np
from sklearn.externals import joblib
from keras.models import load_model

import config
from container import Container


argparse = argparse.ArgumentParser()
argparse.add_argument("-dp", "--datapoints-behind", required=True, dest="datapoints_behind", type=int,
                      help="Datapoints behind to be added for the model on each line")
argparse.add_argument("-hg", "--hour-granularity", required=True, dest="hour_granularity", type=int,
                      help="How many hours a datapoint will agregate")
args = vars(argparse.parse_args())

container = Container()
days_behind = math.ceil(args['datapoints_behind'] * args['hour_granularity'] / 24) * 2
dataframe = container.final_data_provider().get(days_behind, args['datapoints_behind'], args['hour_granularity']).tail(1)
print(dataframe)
dataframe.to_csv('sample_data/one_shot.csv')


scaler = joblib.load(config.model['sklearn_scaler_file_name'])
classifier = load_model(config.model['keras_model_file_name'])

X = dataframe.iloc[:, 1:].values
y_pred = classifier.predict_classes(scaler.transform(np.array([X[0]])))
print(y_pred)