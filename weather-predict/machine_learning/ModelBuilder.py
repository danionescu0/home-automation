from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout


class ModelBuilder:
    def build(self, input_dimensions: int, optimizer: str):
        model = Sequential()
        inner_nodes = int(input_dimensions / 2)
        model.add(Dense(output_dim=inner_nodes, init='uniform', activation='relu', input_dim=input_dimensions))
        model.add(Dropout(p=0.2))
        model.add(Dense(output_dim=inner_nodes, init='uniform', activation='relu'))
        model.add(Dropout(p=0.2))
        model.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))
        model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

        return model