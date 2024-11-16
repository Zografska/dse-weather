import streamlit as st
import pandas as pd
import pydeck as pdk


def traveler_demo():
    @st.cache_data
    def from_data_file(drop_last_column=False):
        url = "../output/result.csv"
        dataset = pd.read_csv(url)
        if drop_last_column:
            return dataset[:-1]
        return dataset

    try:
        ALL_LAYERS = {
            "City Names": pdk.Layer(
                "TextLayer",
                data=from_data_file(drop_last_column=True),
                get_position=["Longitude", "Latitude"],
                get_text="City",
                get_color=[0, 255, 255, 200],
                get_size=13,
                get_alignment_baseline="'bottom'",
            ),
            "Travel Path": pdk.Layer(
                "ArcLayer",
                data=from_data_file(drop_last_column=True),
                get_source_position=["Longitude", "Latitude"],
                get_target_position=["Prev_Longitude", "Prev_Latitude"],
                get_source_color=[246, 204, 0, 80],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0002,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
            "Southern Limit": pdk.Layer(
                "LineLayer",
                data=[{"source": [180, 33.5], "target": [-180, 33.5]}],
                get_source_position="source",
                get_target_position="target",
                get_color=[255, 0, 0],
                get_width=1,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/navigation-night-v1",
                    initial_view_state={
                        "latitude": 45.9,
                        "longitude": 129,
                        "zoom": 4,
                        "pitch": 10,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except Exception as e:
        st.error(
            """
            **Please run the Traveler script first**
            
        """
            % e.reason
        )


st.set_page_config(page_title="Traveler Demo", page_icon="🌍")
st.markdown("# Traveler Demo")
st.sidebar.header("Traveler Demo")
st.write(
    """
        ### Summary of the travel

        Running the Traveler.py script, we get an output file with contains the path
        the traveler needs to take to arrive to Los Angeles, starting from Bejing.
        In this example, the traveler travels on day `2013-08-01`,
        but it can be done for any other date present in the data.

        The data was preprocessed, by discarding all the rows that have no `City`,
        `Average Temperature`, `Longitude` and `Latitude`.

        The date `2013-08-01` was specifically chosen since there is no missing data 
        there.

        To speed up the processing I used the BFS algorithm combined with a heuristic
        which pruned the nodes where the cities had a distance further from the goal
        compared to the current state.
        Additionally I forbid the traveler to go to the previously visited city and
        limited the traveler to not go below the 33.5 latitude hence 
        the `Southern Limit` marker.

        Hence I have arrived to this path:
    """
)

traveler_demo()
