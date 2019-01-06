import argparse
import math

import pandas
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
argparse.add_argument("-faddr", "--from-addr", required=True, dest="from_address", type=str,
                      help="Email from which the alert will be sent")
argparse.add_argument("-fpswd", "--from-password", required=True, dest="from_password", type=str,
                      help="The password of the from email")
argparse.add_argument("-toaddr", "--to-addr", required=True, dest="to_address", type=str,
                      help="Email to which the alert will be sent")
args = vars(argparse.parse_args())

container = Container()
email_notifier = container.email_notifier()
days_behind = 10
dataframe = container.final_data_provider().get(days_behind, args['datapoints_behind'], args['hour_granularity']).tail(1)

scaler = joblib.load(config.model['sklearn_scaler_file_name'])
classifier = load_model(config.model['keras_model_file_name'])

X = dataframe.iloc[:, 1:].values
y_pred = classifier.predict_classes(scaler.transform(np.array([X[0]])))

will_rain = y_pred[0][0]

print("The prediction result is: {0}".format(will_rain))
email_notifier.configure(args['from_address'], args['from_password'])
title = 'Rain status for the next {0} hours is {1}'.format(args['hour_granularity'], str(will_rain))
body = 'This is a predicted alert with Keras'
email_notifier.send(args['to_address'], title, body)