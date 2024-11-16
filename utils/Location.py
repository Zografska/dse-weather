# utility class for location related operations
from math import atan2, radians, sin, cos, sqrt


def transform_latitude(latitude):
    """
    Transforms a latitude string into a float that could range in interval (-90, 90).

    Parameters:
        latitude (str): The latitude string to transform. The string should end with 'N' or 'S'.

    Returns:
        float: The transformed latitude as a float. Returns None if the input string is empty.
    """
    if not latitude:
        return None
    if latitude[-1] == "S":
        latitude = float(latitude[:-1]) * -1
    else:
        latitude = float(latitude[:-1])
    return latitude


def transform_longitude(longitude):
    """
    Transforms a longitude string into a float that could range in interval (-180, 180).

    Parameters:
        longitude (str): The longitude string to transform. The string should end with 'E' or 'W'.

    Returns:
        float: The transformed longitude as a float. Returns None if the input string is empty.
    """
    if not longitude:
        return None
    if longitude[-1] == "W":
        longitude = float(longitude[:-1]) * -1
    else:
        longitude = float(longitude[:-1])
    return longitude


def calculateDistance(lat_x, lon_x, lat_y, lon_y):
    """
    Calculates the distance between two geographical points on the Earth's surface using the Haversine formula.

    Parameters:
        lat_x (float): Latitude of the first point in degrees.
        lon_x (float): Longitude of the first point in degrees.
        lat_y (float): Latitude of the second point in degrees.
        lon_y (float): Longitude of the second point in degrees.

    Returns:
        float: The distance between the two points in kilometers.
    """
    lat1 = radians(lat_x)
    lon1 = radians(lon_x)
    lat2 = radians(lat_y)
    lon2 = radians(lon_y)
    R = 6371.01  # Aproximate of Earth's radius in kilometers
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
