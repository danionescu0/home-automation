from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

from machine_learning.ModelBuilder import ModelBuilder


class GridSearch:
    def __init__(self, model_builder: ModelBuilder) -> None:
        self.__model_builder = model_builder
        self.__parameters = {
            'batch_size': [1,3, 5,7, 8, 20],
            'nb_epoch': [7, 10, 20, 25, 50],
            'optimizer': ['adam', 'rmsprop', 'sgd']
        }

    def search(self, X_train, y_train) -> tuple:
        self.__parameters['input_dimensions'] = [X_train.shape[1]]
        classifier = KerasClassifier(build_fn=self.__model_builder.build)
        grid_search = GridSearchCV(estimator=classifier, param_grid=self.__parameters, scoring='accuracy', cv=5, n_jobs=-1)
        grid_search = grid_search.fit(X_train, y_train)

        return grid_search.best_params_, grid_search.best_score_
