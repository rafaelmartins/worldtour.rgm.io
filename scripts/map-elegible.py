#!/usr/bin/env python2
# coding: utf-8

from utils.kml import render_kml_airport
from utils.ourairports import parse_airports
from utils.xplane import has_scenery

import os

# Aircraft parameters (ToLiss Airbus A319)
ACTF_ICAO = 'A319'
ACFT_MIN_RWY_LENGTH = 1200
ACFT_MIN_RWY_WIDTH = 30

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AIRPORTS_FILE = os.path.join(ROOT_DIR, 'data', 'international-airports.txt')
MAP_FILE = os.path.join(ROOT_DIR, 'data', 'elegible-airports.kml')


def main():
    airports = parse_airports()
    intl_airports = []
    with open(AIRPORTS_FILE) as fp:
        for line in fp:
            if line:
                intl_airports.append(line.strip())

    valid_airports = []

    for icao in intl_airports:
        apt = airports.get(icao)
        if not apt:
            print '%s: BAD: not found' % icao
            continue

        if not apt.runways:
            print '%s: BAD: no runways' % icao
            continue

        fail = False
        for rwy in apt.runways:
            if rwy.length < ACFT_MIN_RWY_LENGTH:
                print '%s: BAD: too short (%s)' % (icao, rwy.name)
                fail = True
                break
            if rwy.width < ACFT_MIN_RWY_WIDTH:
                print '%s: BAD: too narrow (%s)' % (icao, rwy.name)
                fail = True
                break
        if fail:
            continue

        if not has_scenery(icao):
            print '%s: BAD: no scenery' % icao
            continue

        print '%s: GOOD' % icao
        valid_airports.append(apt)

    with open(MAP_FILE, 'w') as fp:
        fp.write(render_kml_airport(valid_airports))


if __name__ == '__main__':
    main()
