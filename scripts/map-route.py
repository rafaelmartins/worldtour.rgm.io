#!/usr/bin/env python2
# coding: utf-8

from utils.conversions import get_distance_in_nm
from utils.kml import render_kml_route
from utils.ourairports import parse_airports

import os

MINIMUM_DISTANCE = 300   # in Nm
MAXIMUM_DISTANCE = 2100  # in Nm


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AIRPORTS_FILE = os.path.join(ROOT_DIR, 'data', 'international-airports.txt')
ROUTE_FILE = os.path.join(ROOT_DIR, 'data', 'route.txt')
MAP_FILE = os.path.join(ROOT_DIR, 'data', 'route.kml')


def main():
    airports = parse_airports()

    with open(ROUTE_FILE) as fp:
        route_list = fp.read().split()

    # validate airports
    origin = None
    valid_airports = []
    for icao in route_list:
        apt = airports.get(icao)
        if not apt:
            continue

        # validate distance
        if origin is not None:
            dist = get_distance_in_nm(origin, apt)
            if dist < MINIMUM_DISTANCE or dist > MAXIMUM_DISTANCE:
                raise RuntimeError(
                    'Flight distance is invalid for %s -> %s: %d Nm' %
                    (origin.icao, apt.icao, dist)
                )
            print '        Distance: %d Nm' % dist

        print '%s -> Runway %s' % (icao, apt.runways)

        valid_airports.append(apt)
        origin = apt

    with open(MAP_FILE, 'w') as fp:
        print >> fp, render_kml_route(valid_airports)


if __name__ == '__main__':
    main()
