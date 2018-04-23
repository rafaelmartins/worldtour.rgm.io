# coding: utf-8

import math


def ft2m(ft):
    if not ft:
        return 0
    return int(ft) * 0.3048


def deg2rad(deg):
    return deg * math.pi / 180


def get_distance_in_km(o, d):
    a = (
        (math.sin(deg2rad(d.lat - o.lat) / 2) ** 2) +
        (
            (math.sin(deg2rad(d.lon - o.lon) / 2) ** 2) *
            math.cos(deg2rad(o.lat)) *
            math.cos(deg2rad(d.lat))
        )
    )
    return 12742 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_distance_in_nm(o, d):
    return get_distance_in_km(o, d) * 0.539957
