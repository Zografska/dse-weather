import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns

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
def filterdata(df, selected_date):
    return df[df["dt"] == selected_date]


@st.cache_data
def countries():
    return from_data_file()["Country"].unique()


st.set_page_config(page_title="Change of Temperature over Time", page_icon="📈")
st.markdown("# Change of Temperature over Time")
st.write(
    """This plot let's you explore the distribution of average temperature over time."""
)
data = from_data_file()
data["dt"] = pd.to_datetime(data["dt"])

filtered_dates = data[data["dt"].dt.strftime("%m").str.contains(r"^(01|08)$")][
    "dt"
].unique()

# show the data in descending order
column_values = sorted(filtered_dates, reverse=True)

bins = st.sidebar.slider("Number of bins", 10, 100, 30)
selected_month = st.sidebar.selectbox(
    "Select a month", column_values, format_func=lambda x: x.strftime("%B %Y")
)

st.write(selected_month)
filtered_data = filterdata(data, selected_month)
st.write("First let's get an overview of the data:")
st.write(
    filtered_data.loc[
        :, ["AverageTemperature", "AverageTemperatureUncertainty"]
    ].describe()
)

plt.hist(
    filtered_data["AverageTemperature"], bins=bins, color="skyblue", edgecolor="black"
)
plt.axvline(
    filtered_data["AverageTemperature"].mean(),
    color="red",
    linestyle="dashed",
    linewidth=1,
)

plt.title(
    f"Average Temperature Distribution on {selected_month.strftime("%B %Y")}",
    fontsize=16,
)
plt.xlabel("Average Temperature (°C)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)

plt.legend(
    ["Sample Mean", "Temperature Distribution"],
    title="Legend",
    title_fontsize="12",
    fontsize="10",
    loc="upper left",
)

st.pyplot(plt)
plt.close()


st.subheader("Comparison of average temperature between countries now and X years ago")

countries = st.multiselect(
    "Choose countries",
    list(countries()),
    ["Cuba", "United States", "Mexico", "Costa Rica"],
)

years_ago = st.slider("Go back in time X years", 10, 100, 10)
history_month = selected_month - pd.DateOffset(years=years_ago)

plot_data = data[
    (data["Country"].isin(countries))
    & ((data["dt"] == history_month) | (data["dt"] == selected_month))
]

# Create a scatter plot
sns.catplot(
    data=plot_data,
    x="dt",
    y="AverageTemperature",
    hue="Country",
    kind="bar",
)


plt.title(
    f"Average Temperature by Country on {selected_month.strftime("%B %Y")}", fontsize=16
)
plt.xlabel("Average Temperature Uncertainty (°C)", fontsize=14)
plt.ylabel("Average Temperature (°C)", fontsize=14)

plt.grid(True, linestyle="--", alpha=0.6)

st.pyplot(plt)
