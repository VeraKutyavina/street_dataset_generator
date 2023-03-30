import math


def get_heading_param(q1, q2):
    start_lat = q1[1]
    start_lon = q1[0]
    end_lat = q2[1]
    end_lon = q2[0]
    azimuth = math.degrees(math.atan2(math.sin(math.radians(end_lon - start_lon)) * math.cos(math.radians(end_lat)),
                                      math.cos(math.radians(start_lat)) * math.sin(math.radians(end_lat)) - math.sin(
                                          math.radians(start_lat)) * math.cos(math.radians(end_lat)) * math.cos(
                                          math.radians(end_lon - start_lon))))

    heading = 90 - azimuth
    return heading
