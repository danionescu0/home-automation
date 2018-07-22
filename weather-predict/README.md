## Weather prediction using machine learning (keras with tensorflow) and local weather data from the weather station


The input data will previous information gathered locally from the weather station on the following sensors:

- temperature 

- humidity

- pressure

- light

- rain levels

The output data will be prediction on rain levels for the next N hours

Currently i've tested the model on 6 h and it has 80-82% accuracy

Steps:

1. Generate the basic data using data_extractor.py

For example:

````
python data_extractor.py --output-file some_file.csv --day-behind nr_days --hour-granularity granularity <= 24
````

This will extract data from the home automation repository and save it in a csv format.


2. Generate the model using data_enhancer.py and show also the test values

````
python data_enhancer.py --input-file weather.csv --test-file-percent 6 --datapoints-behind 10
````
This will enhance the generated model and split it in two files a main file and a test file

The enhancements are:

- days with mean temperatures below 0 are excluded. The exclusions happen because
temperatures below zero means rain will turn into snow, and the weather station doesn't detect snow

- a boolean 0/1 has_rain is includen in the columns based on average rain

- the N previous rows are added for every row for model consistency

3. Train the model

````
python training.py --input-file file_name --test-file test_file_name --mode [grid|test]
````

For mode grid it will make a grid search with the parameters wich are best

For test mode it will use the test_file_name to load data and calculate predictions 