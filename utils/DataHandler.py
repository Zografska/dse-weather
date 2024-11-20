import os

import pandas as pd


class DataHandler:
    """
    Data structure consisting of tools to analyse and clean the data

    Parameters
    ----------
    path: str
        A path pointing to the file with data.
    """

    def __init__(self, path):
        self.dataframe = pd.read_csv(path)

    def explore(self):
        print("General Info")
        self.dataframe.info()
        print(self.dataframe.describe())
        print("Check amount of null values for each feature")
        print(self.dataframe.isnull().sum())

    def clean(self, feature):
        self.dataframe = self.dataframe.dropna(subset=feature)
        # restore indexes
        self.dataframe = self.dataframe.reset_index(drop=True)
