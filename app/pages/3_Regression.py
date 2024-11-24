import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src import DataHandler as dh


@st.cache_data
def from_data_file():
    data_handler = dh.DataHandler("../data/GlobalLandTemperaturesByCountry.csv")
    data_handler.clean("AverageTemperature")
    data_handler.clean("Country")
    data_handler.clean("dt")
    return data_handler.dataframe


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


def get_data_for_country(data, country):
    data_country = data[data["Country"] == country][["dt", "AverageTemperature"]]
    variable_name = f"AverageTemperature_{country}"
    data_country = data_country.rename(columns={"AverageTemperature": variable_name})
    return data_country, variable_name


st.set_page_config(page_title="Linear Regression", page_icon="📈")
st.markdown("# Linear Regression")
st.write(
    """Here you can check out the linear regression between two countries' average temperatures."""
)
data = from_data_file()

list_of_countries = countries()

country_x = st.sidebar.selectbox(
    label="Select the first country", options=list_of_countries, index=107
)
country_y = st.sidebar.selectbox(
    label="Select the other country", options=list_of_countries, index=128
)

test_size = st.sidebar.slider("Test Set Size (%)", 0, 100, 25) / 100

[data_x, name_x] = get_data_for_country(data, country_x)
[data_y, name_y] = get_data_for_country(data, country_y)

# Merge the dataframes to have data for the same dates
merged_data = pd.merge(data_x, data_y, on="dt", how="inner")

X = np.array(merged_data[name_x]).reshape(-1, 1)
y = np.array(merged_data[name_y]).reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

regr = LinearRegression()

regr.fit(X_train, y_train)
regression_score = regr.score(X_test, y_test)
st.write(f"Regression score: {regression_score}")

y_pred = regr.predict(X_test)
plt.scatter(X_test, y_test, color="teal", marker="o", alpha=0.5, label="Test data")
plt.plot(X_test, y_pred, color="red", label="Regression line")

plt.title(
    f"Linear Regression of Average Temperatures: {country_x} vs. {country_y}",
    fontsize=12,
    weight="bold",
)
plt.xlabel(f"Average Temperature in {country_x} (°C)", fontsize=12)
plt.ylabel(f"Average Temperature in {country_y} (°C)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
# Customize the legend
plt.legend(title="Legend", title_fontsize="13", fontsize="11", loc="upper left")

st.pyplot(plt)
