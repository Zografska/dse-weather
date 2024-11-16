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
        - 1. 🌍 Home
        - 2. 📊 Data Analysis
        - 3. 🗺️ Traveler - Visualize the path of a traveler that prefers warm weather. They usually jump to one of the closest 3 cities which has the best weather. The goal is to arrive to Los Angeles, USA 🌴, starting from Peking, China 🇨🇳
            - This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data.

        ### Tasks:
        - [x] 1. 🛠️ Usage of GitHub
        - [ ] 2. 🗂️ Correct modularisation
        - [ ] 3. 📥 Import and output of data
        - [x] 4. 🐼 Usage of a data manipulation library (e.g. pandas)
        - [ ] 5. 🔢 Usage of a scientific computing library (e.g. numPy)
        - [ ] 6. 📊 Usage of a data visualization library (e.g. matplotlib)
        - [x] 7. 🌟 BONUS - Usage of a web app creation framework (e.g. streamlit) [Streamlit](https://streamlit.io/)
    """
    )


if __name__ == "__main__":
    run()
