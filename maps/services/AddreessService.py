import math


def get_heading_param(point1, point2):
    start_lon = point1[0]
    start_lat = point1[1]
    end_lon = point2[0]
    end_lat = point2[1]
    azimuth = math.degrees(math.atan2(math.sin(math.radians(end_lon - start_lon)) * math.cos(math.radians(end_lat)),
                                      math.cos(math.radians(start_lat)) * math.sin(math.radians(end_lat)) - math.sin(
                                          math.radians(start_lat)) * math.cos(math.radians(end_lat)) * math.cos(
                                          math.radians(end_lon - start_lon))))

    return azimuth
