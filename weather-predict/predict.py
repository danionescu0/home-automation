import sys
import pandas as pd
import numpy

from ModelPreparator import ModelPreparator
from learning import get_dnn_regressor, wx_input_fn


file_name = sys.argv[1]

model_preparator = ModelPreparator()
original_dataframe = model_preparator.prepare(pd.read_csv(file_name))
dataframe = original_dataframe.drop(['has_rain'], axis=1)
regressor = get_dnn_regressor(dataframe)

pred = regressor.predict(input_fn=wx_input_fn(dataframe, num_epochs=1, shuffle=False))
predictions = numpy.array([p['predictions'][0] for p in pred])

for index, prediction in enumerate(predictions):
    print("Date: {0}, Actual: {1}, Predicted: {2}"
          .format(original_dataframe.iloc[index].name, original_dataframe.iloc[index]['rain_outside_max'], prediction))

