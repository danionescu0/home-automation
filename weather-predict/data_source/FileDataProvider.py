import pandas as pd


class FileDataProvider:
    def get(self, path: str) -> tuple:
        dataset = pd.read_csv(path)
        X = dataset.iloc[:, 2:].values
        y = dataset.iloc[:, 1].values

        return X, y