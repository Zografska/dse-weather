import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.utils import from_data_file, countries


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

bins = st.sidebar.slider("Number of bins", 10, 100, 30)
selected_month = st.sidebar.selectbox(
    "Select a month", column_values, format_func=lambda x: x.strftime("%B %Y")
)

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
    ["Italy", "France", "Russia", "Macedonia"],
)

years_ago = st.slider("Go back in time X years", 10, 100, 10)
past_data = selected_month - pd.DateOffset(years=years_ago)

plot_data = data[
    (data["Country"].isin(countries))
    & ((data["dt"] == past_data) | (data["dt"] == selected_month))
]

# Create a scatter plot
sns.catplot(
    data=plot_data,
    x="dt",
    y="AverageTemperature",
    hue="Country",
    kind="bar",
    palette="flare",
)


plt.title(
    f"{selected_month.strftime('%B %Y')} vs. {selected_month.strftime('%B %Y')}",
    fontsize=16,
)

plt.ylabel("Average Temperature (°C)", fontsize=14)

x_dates = plot_data["dt"].dt.strftime("%B %Y").sort_values().unique()
plt.xticks(ticks=range(len(x_dates)), labels=x_dates)

plt.grid(True, linestyle="--", alpha=0.6)

st.pyplot(plt)
