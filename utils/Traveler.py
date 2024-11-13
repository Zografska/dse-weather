import os

import pandas as pd
from math import atan2, radians, sin, cos, acos, sqrt

import DataHandler as dh


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
traveler = Traveler("Peking")
# temperature_by_city_data.clean(feature="AverageTemperature")
temperature_by_city_data.clean(feature="City")

# china_city = temperature_by_city_data.dataframe[
#     temperature_by_city_data.dataframe["City"] == "Shunyi"
# ].sort_values("dt")
# print(china_city.tail(10))

print(temperature_by_city_data.dataframe["City"].unique().__len__())

# transform the data
temperature_by_city_data.dataframe["Latitude"] = temperature_by_city_data.dataframe[
    "Latitude"
].transform(lambda x: float(x[:-1]))
temperature_by_city_data.dataframe["Longitude"] = temperature_by_city_data.dataframe[
    "Longitude"
].transform(lambda x: float(x[:-1]))


starting_point = (
    temperature_by_city_data.dataframe.where(
        temperature_by_city_data.dataframe["City"] == "Peking"
    )
    .dropna()
    .reset_index()
)


starting_location = starting_point.loc[0, ["Latitude", "Longitude"]]

# print(starting_location)
grouped = temperature_by_city_data.dataframe.groupby(
    temperature_by_city_data.dataframe["dt"]
)["City"]

print(grouped.nunique())

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


visited = []
queue = []

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

# def getNeighbours(dataset, location, )

travel_dataset["distance"] = travel_dataset.apply(
    lambda row: calculateDistance(
        row["Latitude"],
        row["Longitude"],
        starting_location["Latitude"],
        starting_location["Longitude"],
    ),
    axis=1,
)
travel_dataset = travel_dataset.sort_values(by="distance", ascending=True)
print(travel_dataset.head(3))


# print(three_closest.head(3))
