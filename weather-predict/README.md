## Weather prediction using machine learning (keras with tensorflow) and local weather data from the weather station


The input data will previous information gathered locally from the weather station on the following sensors:

- temperature 

- humidity

- pressure

- light

- rain levels

# Installation
You could use anaconda for the installation:
````
conda create --name ml python=3.6.2
conda activate ml
pip install theano
pip install tensorflow
pip install keras
pip install pandas
pip install sklearn
pip install requests
pip install pymongo
conda update --all
conda activate ml
````

The output data will be prediction on rain levels for the next N hours

Currently i've tested the model on 6 h and it has over 85% accuracy

Steps:

1. Import data

````
python import_from_home_automation.py --day-behind nr_days
````

This will extract data from the home automation repository and save it into the local mongoDb database


2. Generate the model 
````
python train.py --days_behind 600 --test-file-percent 10 --datapoints-behind 6 --hour-granularity 6
````

Parameters:

--days_behind : how many days in the past shoul be taken into account when generating the model

--test-file-percent : percent of the data to generate a file with
 
--datapoints-behind : each entry in the training data will contain historical data (a few datapoints from the past)

--hour-granularity : each datapoint of traiing data will be created from a defined amount of hours grouped togeather

[optional] --grid-search : if set this parameter will trigger a "grid search" to find the optimal parameters for our dataset
It will try diffrerent options for: batch_size, nb_epoch, optimizer and dropout

4. Predict batch [optional]
This will try to predict if it rains or not for the data generated in data_soruce/test_data.csv

````
python predict_batch.py 
````

5. Predict if it will rain in the next few hours

````
python predict.py --datapoints-behind 6 --hour-granularity 6
````

# How does it work

- raw data that is coming from the weather station is stored in a mongoDb database
- when the model is generated, data is exported from mongoDb into a pandas dataframe and it's augmented like this:
1. nan values are dropped
2. the data is grouped and aditional metrics are constructed along the way. 
````
#the dataframe columns before:

"date", "pressure", "humidity", "temperature", "light", "rain"

#dataframe columns after:
"date", "pressure", "pressure_min", "pressure_min", "pressure_max", "pressure_avg", "pressure_raise", "pressure_fall", "pressure_steady", "pressure_percentile90", .."humidity",.. "temperature",... "light",... "rain"
````
3. a new dataframe column is added "has_rain" based of the "rain_avg" columns it will be 0 or 1
4. "date" column is dropped
5. all rows whose "rain_avg" are below 0 will be dropped because we don't have a snow sensor and the data will be useless
6. for each row new columns are added to reference the previous rows
````
#the dataframe columns before:
"pressure", "pressure_min", "pressure_min", "pressure_max"....

#dataframe columns after:
"has_rain", "pressure", "pressure_min", ... "has_rain_1", "pressure_1", "pressure_min_1"... "has_rain_2", "pressure_2", "pressure_min_2"..

# has_rain_1 means the previous has_rain datapoint

````
7. first "datapoints-behind" rows from the whole dartaframe are dropped because will conain incomplete values
8. "pressure", "pressure_min" .. "pressure_avg".. are dropped, because we need to predict if it's going to rain without knowing the current temperature, pressure etc.

All we'll know is's the previous datapoints embeded in the row.

- the dataframe is scaled using sklearn StandardScaler
- after the dataframe is complete the Keras model is compiled built, and trained
- the keras model and StandardScaler are saved in files so they can be reused
