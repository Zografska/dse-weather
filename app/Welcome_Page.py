import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Aleksandra's Traveler",
        page_icon="👋🗺️",
    )

    st.write("# Welcome to Aleksandra's presentation! 👋")

    st.markdown(
        """
        ### 🌍 **Weather dataset project** 
        ### Dataset:
        🔗 [Climate Change Earth Surface Temperature Data](https://kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)
        ### Pages:
        1. 🌍 Welcome page
        2. 🗺️ Traveler 
            - Visualize the path of a traveler that prefers warm weather. They usually jump to one of the closest 3 cities which has the best weather. The goal is to arrive to Los Angeles, USA 🌴, starting from Peking, China 🇨🇳
        3. 📊 Interactive Plots
    """
    )


if __name__ == "__main__":
    run()
