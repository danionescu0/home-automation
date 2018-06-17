import sys
import pandas as pd
import numpy
import tensorflow as tf
from ModelPreparator import ModelPreparator


file_name = sys.argv[1]

model_preparator = ModelPreparator()
original_dataframe = model_preparator.prepare(pd.read_csv(file_name))
dataframe = original_dataframe.drop(['rain_outside_max'], axis=1)

feature_cols = [tf.feature_column.numeric_column(col) for col in dataframe.columns]

regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                      hidden_units=[50, 50],
                                      model_dir='tf_rain_model')

def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):
    return tf.estimator.inputs.pandas_input_fn(x=X,
                                               y=y,
                                               num_epochs=num_epochs,
                                               shuffle=shuffle,
                                               batch_size=batch_size)

pred = regressor.predict(input_fn=wx_input_fn(dataframe,
                                              num_epochs=1,
                                              shuffle=False))
predictions = numpy.array([p['predictions'][0] for p in pred])

for index, prediction in enumerate(predictions):
    print("Date: {0}, Actual: {1}, Predicted: {2}"
          .format(original_dataframe.iloc[index].name, original_dataframe.iloc[index]['rain_outside_max'], prediction))

