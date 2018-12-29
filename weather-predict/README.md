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

For example:

````
python import_from_home_automation.py --day-behind nr_days
````

This will extract data from the home automation repository and save it into the local mongoDb database


2. Generate the model 
````
python train.py -d 600 -p 10 -dp 6 -hg 6
````



- days with mean temperatures below 0 are excluded. The exclusions happen because
temperatures below zero means rain will turn into snow, and the weather station doesn't detect snow

- a boolean 0/1 has_rain is includen in the columns based on average rain

- the N previous rows are added for every row for model consistency

For mode grid it will make a grid search with the parameters wich are best

4. Predict batch
````
python predict_batch.py --test-file test_file_name 
````