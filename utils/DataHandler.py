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
        self.path = os.path.join(f"./data/{path}", "")
        self.dataframe = pd.read_csv(path)

    @property
    def export_data(self):
        self.dataframe.to_csv(f"./output/{self.path}_output.csv")

    @property
    def explore(self):
        print("General Info")
        self.dataframe.info()
        print(self.dataframe.describe())
        print("Check amount of null values for each feature")
        print(self.dataframe.isnull().sum())
