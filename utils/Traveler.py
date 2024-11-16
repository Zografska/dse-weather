import os
import string

import pandas as pd
from math import atan2, radians, sin, cos, acos, sqrt

import DataHandler as dh


def transform_latitude(latitude):
    if not latitude:
        return None
    if latitude[-1] == "S":
        latitude = float(latitude[:-1]) * -1
    else:
        latitude = float(latitude[:-1])
    return latitude


def transform_longitude(longitude):
    if not longitude:
        return None
    if longitude[-1] == "W":
        longitude = float(longitude[:-1]) * -1
    else:
        longitude = float(longitude[:-1])
    return longitude


def calculateDistance(lat_x, lon_x, lat_y, lon_y):
    lat1 = radians(lat_x)
    lon1 = radians(lon_x)
    lat2 = radians(lat_y)
    lon2 = radians(lon_y)
    R = 6371.01
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


class Traveler:
    def __init__(self, starting_city):
        self.start = starting_city
        self.current_position = starting_city


temperature_by_city_data = dh.DataHandler("./data/GlobalLandTemperaturesByCity.csv")
temperature_by_city_data.clean(feature="Latitude")
temperature_by_city_data.clean(feature="Longitude")
traveler = Traveler("Peking")
# temperature_by_city_data.clean(feature="AverageTemperature")
temperature_by_city_data.clean(feature="City")

# china_city = temperature_by_city_data.dataframe[
#     temperature_by_city_data.dataframe["City"] == "Shunyi"
# ].sort_values("dt")
# print(china_city.tail(10))

# print(temperature_by_city_data.dataframe["City"].unique().__len__())

# transform the data
temperature_by_city_data.dataframe["Latitude"] = temperature_by_city_data.dataframe[
    "Latitude"
].transform(lambda x: transform_latitude(x))
temperature_by_city_data.dataframe["Longitude"] = temperature_by_city_data.dataframe[
    "Longitude"
].transform(lambda x: transform_longitude(x))


starting_point = (
    temperature_by_city_data.dataframe.where(
        temperature_by_city_data.dataframe["City"] == "Peking"
    )
    .dropna()
    .reset_index()
)


starting_location = starting_point.loc[0, ["Latitude", "Longitude", "City"]]

# print(starting_location)
grouped = temperature_by_city_data.dataframe.groupby(
    temperature_by_city_data.dataframe["dt"]
)["City"]

# print(grouped.nunique())


# counting the unique cities
# grouping the data by date and filtering on unique 'city' values
# we see that on 2013-09-01 we have the same count of records
# as number of unique cities
# so we can choose that year as our travel year

travel_dataset = temperature_by_city_data.dataframe
mask = travel_dataset["dt"] == "2013-08-01"
travel_dataset = travel_dataset[mask]
# print(travel_dataset)
# starting_location = [float(x[:-1]) for x in starting_location_raw]

# ne raboti
# three_closest = travel_dataset.sort_values(
#     by=["Latitude", "Longitude"],
#     key=lambda x: (
#         calculateDistance(
#             x.Latitude,
#             x.Longitude,
#             1,
#             2,
#         )
#     ),
# )


# get first tree closest
def get_neighbours(dataset, location):
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

    destination = dataset[
        (dataset["City"] == "Los Angeles") & (dataset["distance"] == 0)
    ]
    if destination.__len__():
        return [destination, "arrived"]

    dataset = dataset[
        (dataset["City"] != location["City"]) & (dataset["distance"] != 0)
    ]

    dataset = dataset.sort_values(
        by=["distance", "AverageTemperature"], ascending=[True, False]
    ).reset_index()

    return [dataset.head(10), "travelling"]


path = []
# travel_dataset["Visited"] = "No"
[neighbours, status] = get_neighbours(travel_dataset, starting_location)


visited = []
queue = []


## find path to destination bfs
def bfs(visited, travel_dataset, node):
    visited.append(node["City"])
    queue.append([node, [node["City"]], []])

    while queue:
        [current, path, visited] = queue.pop(0)
        # visited = visited + [current["City"]]
        [neighbours, status] = get_neighbours(travel_dataset, current)
        # print(current["City"])
        print(
            f"i am travelling from {current['City']}, already passed {','.join(visited)} cities"
        )
        if status == "arrived":
            print(neighbours)
            print(path)
            print(visited)
            break

        for _, neighbour in neighbours.iterrows():
            if neighbour["City"] not in path:
                city_name = current["City"]
                queue.append([neighbour, path + [city_name], visited + [city_name]])


bfs(visited, travel_dataset, starting_location)


# while status == "travelling":
#     to_visit = neighbours.loc[neighbours["Visited"] == "No"].iloc[0]
#     path.append(to_visit)
#     print(to_visit["City"])
#     travel_dataset.loc[travel_dataset["City"] == to_visit["City"], "Visited"] = "Yes"
#     [neighbours, status] = get_neighbours(travel_dataset, to_visit)

print(path.__len__())


# print(three_closest.head(3))
