import pandas
import numpy
from sklearn.externals import joblib
from keras.models import load_model

import config


scaler = joblib.load(config.model['sklearn_scaler_file_name'])
classifier = load_model(config.model['keras_model_file_name'])

dataset = pandas.read_csv(config.model['test_data_file']).set_index('_id')
X = dataset.iloc[:, 1:].values
y = dataset.iloc[:, 0].values

total = predicted_good_total = 0
nr_rainy_days = predicted_good_rainy_days = 0

for test_data in X:
    y_pred = classifier.predict_classes(scaler.transform(numpy.array([test_data])))
    actual_rain = True if y[total] == 1 else False
    predicted_rain = y_pred > 0
    if actual_rain is True:
        nr_rainy_days += 1
        predicted_good_rainy_days += 1 if actual_rain == predicted_rain else 0
    predicted_good_total += 1 if predicted_rain == actual_rain else 0
    mark_predicted_badly = '#' if actual_rain != predicted_rain else ''
    print("Index: {0}, Actual / Predicted: {1}{2} / {3}{4}". format(total, mark_predicted_badly, actual_rain,
                                                                     predicted_rain[0][0], mark_predicted_badly))
    total += 1

print ('Standard: Total: {0}, Good: {1}, Percent accuracy: {2} '.
       format(total, predicted_good_total, predicted_good_total * 100 / total))
print ('False negatives penalty: Total: {0}, Good: {1}, Percent accuracy: {2} '.
       format(nr_rainy_days, predicted_good_rainy_days, predicted_good_rainy_days * 100 / nr_rainy_days))

print(classifier.evaluate(X, y, verbose=1))
