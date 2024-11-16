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

goal = (
    temperature_by_city_data.dataframe.where(
        (temperature_by_city_data.dataframe["City"] == "Los Angeles")
        & (temperature_by_city_data.dataframe["Country"] == "United States")
    )
    .dropna()
    .reset_index()
).iloc[0]

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
)


starting_location = starting_point.iloc[0]

grouped = temperature_by_city_data.dataframe.groupby(
    temperature_by_city_data.dataframe["dt"]
)["City"]


# counting the unique cities
# grouping the data by date and filtering on unique 'city' values
# we see that on 2013-09-01 we have the same count of records
# as number of unique cities
# so we can choose that year as our travel year


travel_dataset = temperature_by_city_data.dataframe

mask = travel_dataset["dt"] == "2013-08-01"
travel_dataset = travel_dataset[mask]


# get first tree closest
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

    has_arrived = dataset[
        (dataset["City"] == "Los Angeles") & (dataset["distance"] == 0)
    ]
    if has_arrived.__len__():
        return [has_arrived, "arrived"]

    dataset = dataset[
        (dataset["City"] != location["City"]) & (dataset["distance"] != 0)
    ]

    dataset = dataset[dataset["Latitude"] > 33.5]
    dataset = dataset[dataset["distance_to_goal"] < location["distance_to_goal"]]

    dataset = dataset.sort_values(
        by=["distance", "AverageTemperature"],
        ascending=[True, False],
    ).reset_index()

    return [dataset.head(3), "travelling"]


## find path to destination bfs
def bfs(travel_dataset, node):
    visited = []
    visited.append(node["City"])
    path = []
    queue = []
    queue.append([node, [node["City"]], []])
    closest = node["distance_to_goal"]

    while queue:
        [current, path, visited] = queue.pop(0)
        [neighbours, status] = get_neighbours(travel_dataset, current, goal)

        if current["City"] == "Los Angeles":
            print(neighbours)
            print(path)
            return path

        if current["distance_to_goal"] < closest:
            closest = current["distance_to_goal"]
            queue = [node for node in queue if node[0]["distance_to_goal"] <= closest]
            print(
                f"closest is {current['City']} with distance {current['distance_to_goal']}"
            )

        if current["Country"] == "United States":
            print(f"I stepped in the US in city {current['City']}")
            print(neighbours)
            queue = [node for node in queue if node[0]["Country"] == "United States"]

        print(
            f"i am travelling from {current['City']}, already passed {','.join(path)} cities, distance to goal is {current['distance_to_goal']}"
        )

        for _, neighbour in neighbours.iterrows():
            if neighbour["City"] not in path:
                city_name = current["City"]
                queue.append([neighbour, path + [city_name], visited + [city_name]])


path = bfs(travel_dataset, starting_location)
print(f"Path to Los Angeles is {path}")
