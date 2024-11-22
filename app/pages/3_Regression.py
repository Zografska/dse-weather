import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from utils import DataHandler as dh


@st.cache_data
def from_data_file():
    data_handler = dh.DataHandler("../data/GlobalLandTemperaturesByCountry.csv")
    data_handler.clean("AverageTemperature")
    data_handler.clean("Country")
    data_handler.clean("dt")
    return data_handler.dataframe


@st.cache_data
def filterdata(df, selected_date):
    return df[df["dt"] == selected_date]


st.set_page_config(page_title="Linear Regression", page_icon="📈")
st.markdown("# Linear Regression")
st.write("""Please select distributions""")
data = from_data_file()

countries = st.multiselect(
    "Choose countries",
    list(data["Country"].unique()),
    ["Italy", "Spain"],
)

# country_data = data.copy()
# for country in countries:
#     country_df = data[data["Country"] == country][["dt", "AverageTemperature"]]
#     country_df = country_df.rename(columns={"AverageTemperature": f"AverageTemperature_{country}"})
#     pd.merge(country_data, country_df, on="dt", how="left")

data_spain = data[data["Country"] == "Spain"][["dt", "AverageTemperature"]]
data_italy = data[data["Country"] == "Italy"][["dt", "AverageTemperature"]]

data_spain = data_spain.rename(
    columns={"AverageTemperature": "AverageTemperature_Spain"}
)
data_italy = data_italy.rename(
    columns={"AverageTemperature": "AverageTemperature_Italy"}
)

# Merge the dataframes to have data for the same dates
merged_data = pd.merge(data_spain, data_italy, on="dt", how="inner")

X = np.array(merged_data["AverageTemperature_Italy"]).reshape(-1, 1)
y = np.array(merged_data["AverageTemperature_Spain"]).reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

regr = LinearRegression()

regr.fit(X_train, y_train)
regression_score = regr.score(X_test, y_test)
st.write(f"Regression score: {regression_score}")


y_pred = regr.predict(X_test)
plt.scatter(X_test, y_test, color="teal", marker="o", alpha=0.5, label="Test data")
plt.plot(X_test, y_pred, color="red", label="Predicted values")

plt.title(
    "Linear Regression of Average Temperatures: Italy vs. Spain",
    fontsize=12,
    weight="bold",
)
plt.xlabel("Average Temperature in Italy (°C)", fontsize=12)
plt.ylabel("Average Temperature in Spain (°C)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
# Customize the legend
plt.legend(title="Legend", title_fontsize="13", fontsize="11", loc="upper left")

# Hack: https://stackoverflow.com/questions/56656777/userwarning-matplotlib-is-currently-using-agg-which-is-a-non-gui-backend-so
plt.savefig("image-results/regression.png")
st.image("image-results/regression.png")
# Data scatter of predicted values
