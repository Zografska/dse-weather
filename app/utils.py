import os
import sys
import streamlit as st


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import DataHandler as dh


@st.cache_data
def countries():
    countries = from_data_file()["Country"].unique()
    # remove continents
    return [
        country
        for country in countries
        if country
        not in [
            "Africa",
            "Europe",
            "Asia",
            "South America",
            "North America",
            "Antarctica",
        ]
    ]


@st.cache_data
def from_data_file():
    data_handler = dh.DataHandler("../data/GlobalLandTemperaturesByCountry.csv")
    data_handler.clean("AverageTemperature")
    data_handler.clean("Country")
    data_handler.clean("dt")
    return data_handler.dataframe
