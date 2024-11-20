import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns

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
selected_month = st.sidebar.selectbox(
    "Select a month", column_values, format_func=lambda x: x.strftime("%B %Y")
)

filtered_data = filterdata(data, selected_month)

fig, ax = plt.subplots()
ax.hist(
    filtered_data["AverageTemperature"], bins=30, color="skyblue", edgecolor="black"
)

ax.set_title(
    f"Average Temperature Distribution on {selected_month.strftime("%B %Y")}",
    fontsize=16,
)
ax.set_xlabel("Average Temperature (°C)", fontsize=14)
ax.set_ylabel("Frequency", fontsize=14)

st.pyplot(fig)
all_countries = filtered_data["Country"].unique()

countries = st.multiselect(
    "Choose countries",
    list(all_countries),
    ["Cuba", "United States", "Mexico", "Costa Rica"],
)

plot_data = filtered_data[filtered_data["Country"].isin(countries)]

# Create a scatter plot
fig, ax = plt.subplots(figsize=(12, 8))
sns.scatterplot(
    data=plot_data,
    x="AverageTemperatureUncertainty",
    y="AverageTemperature",
    hue="Country",
    palette="tab10",
    ax=ax,
    s=200,
    edgecolor="black",
    linewidth=0.8,
    markers="h",
)


ax.set_title(
    f"Average Temperature by Country on {selected_month.strftime("%B %Y")}", fontsize=20
)
ax.set_xlabel("Average Temperature Uncertainty (°C)", fontsize=16)
ax.set_ylabel("Average Temperature (°C)", fontsize=16)

ax.grid(True, linestyle="--", alpha=0.6)

ax.legend(title="Country", title_fontsize="13", fontsize="11", loc="upper right")

st.pyplot(fig)
