import DataHandler as dh
from Location import calculateDistance, transform_latitude, transform_longitude


class Traveler:
    def __init__(self, starting_city):
        self.start = starting_city
        self.current_position = starting_city


temperature_by_city_data = dh.DataHandler("./data/GlobalLandTemperaturesByCity.csv")
temperature_by_city_data.clean(feature="Latitude")
temperature_by_city_data.clean(feature="Longitude")
traveler = Traveler("Peking")
temperature_by_city_data.clean(feature="City")

# transform the data
temperature_by_city_data.dataframe["Latitude"] = temperature_by_city_data.dataframe[
    "Latitude"
].transform(lambda x: transform_latitude(x))
temperature_by_city_data.dataframe["Longitude"] = temperature_by_city_data.dataframe[
    "Longitude"
].transform(lambda x: transform_longitude(x))

date_of_travel = "2013-08-01"

travel_dataset = temperature_by_city_data.dataframe.copy()
# get data for the date of travel
travel_dataset = travel_dataset[travel_dataset["dt"] == date_of_travel]


# find the goal in the dataset
goal = (
    temperature_by_city_data.dataframe.where(
        (temperature_by_city_data.dataframe["City"] == "Los Angeles")
        & (temperature_by_city_data.dataframe["Country"] == "United States")
    )
    .dropna()
    .reset_index()
).iloc[0]

# create a new column with the distance to the goal
# this will be used as a heuristic so it could reach the goal faster
temperature_by_city_data.dataframe["distance_to_goal"] = (
    temperature_by_city_data.dataframe.apply(
        lambda row: calculateDistance(
            row["Latitude"],
            row["Longitude"],
            goal["Latitude"],
            goal["Longitude"],
        ),
        axis=1,
    )
)

starting_point = (
    temperature_by_city_data.dataframe.where(
        temperature_by_city_data.dataframe["City"] == "Peking"
    )
    .dropna()
    .reset_index()
).iloc[0]


# get the three closest neighbours or the goal if it is reached
# the neighbours are sorted by distance and then by temperature
# heuristic: neighbours that are further away from the goal are discarded
def get_neighbours(dataset, location, goal):
    dataset = dataset.copy()
    dataset["distance"] = dataset.apply(
        lambda row: calculateDistance(
            row["Latitude"],
            row["Longitude"],
            location["Latitude"],
            location["Longitude"],
        ),
        axis=1,
    )

    dataset["distance_to_goal"] = dataset.apply(
        lambda row: calculateDistance(
            row["Latitude"],
            row["Longitude"],
            goal["Latitude"],
            goal["Longitude"],
        ),
        axis=1,
    )

    at_destination = dataset[
        (dataset["City"] == "Los Angeles") & (dataset["distance"] == 0)
    ]
    if at_destination.__len__():
        return at_destination

    dataset = dataset[
        (dataset["City"] != location["City"]) & (dataset["distance"] != 0)
    ]

    # don't wander off below Lattitude 33.5 since L.A. is at 34.05
    dataset = dataset[dataset["Latitude"] > 33.5]
    dataset = dataset[dataset["distance_to_goal"] < location["distance_to_goal"]]

    # sort by distance to the current city and then by temperature
    dataset = dataset.sort_values(
        by=["distance", "AverageTemperature"],
        ascending=[True, False],
    ).reset_index()

    return dataset.head(3)


## find path to destination bfs
def bfs(travel_dataset, node):
    path = []
    queue = []
    queue.append([node, []])
    closest = node["distance_to_goal"]

    while queue:
        [current, path] = queue.pop(0)
        neighbours = get_neighbours(travel_dataset, current, goal)

        if current["City"] == "Los Angeles":
            return path

        if current["distance_to_goal"] < closest:
            closest = current["distance_to_goal"]
            queue = [node for node in queue if node[0]["distance_to_goal"] <= closest]

        if current["Country"] == "United States":
            queue = [node for node in queue if node[0]["Country"] == "United States"]

        for _, neighbour in neighbours.iterrows():
            if neighbour["City"] not in path:
                city_name = current["City"]
                queue.append([neighbour, path + [city_name]])


path = bfs(travel_dataset, starting_point)

# Filter the DataFrame to include only the cities in the 'path' list
filtered_cities = travel_dataset[travel_dataset["City"].isin(path)]

# Append the goal to the DataFrame
filtered_cities = filtered_cities._append(goal)
path.append("Los Angeles")

# Sort the DataFrame by the order of cities in the 'path' list
filtered_cities = filtered_cities.set_index("City").loc[path].reset_index()

# Add new columns with the Latitude and Longitude of the previous row
filtered_cities["Prev_Latitude"] = filtered_cities["Latitude"].shift(-1)
filtered_cities["Prev_Longitude"] = filtered_cities["Longitude"].shift(-1)

# We don't need the last row anymore
# filtered_cities = filtered_cities[:-1]

filtered_cities.to_csv("./output/result.csv", index=False)
print(f"Path to Los Angeles is {path}")
