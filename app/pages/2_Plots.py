import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


@st.cache_data
def from_data_file():
    url = "../data/GlobalLandTemperaturesByCountry.csv"
    dataset = pd.read_csv(url)
    return dataset


@st.cache_data
def filterdata(df, selected_date):
    return df[df["dt"] == selected_date]


st.set_page_config(page_title="Change of Temperature over Time", page_icon="📈")
st.markdown("# Change of Temperature over Time")
st.sidebar.header("Change of Temperature over Time")
st.write(
    """This plot let's you explore the distribution of average temperature over time."""
)
data = from_data_file()

column_values = data.sort_values("dt", ascending=False)["dt"].unique()
selected_day = st.sidebar.selectbox("Select a day", column_values)

arr = filterdata(data, selected_day)["AverageTemperature"]
arr = arr.dropna()

fig, ax = plt.subplots()
ax.hist(arr, bins=30, color="skyblue", edgecolor="black")

ax.set_title(f"Average Temperature Distribution on {selected_day}", fontsize=16)
ax.set_xlabel("Average Temperature (°C)", fontsize=14)
ax.set_ylabel("Frequency", fontsize=14)

st.pyplot(fig)
