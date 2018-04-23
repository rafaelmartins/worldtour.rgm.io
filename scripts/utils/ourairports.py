# coding: utf-8

import os
import re
import requests
from collections import OrderedDict
from csv import DictReader

from .conversions import ft2m

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
AIRPORTS_FILE = os.path.join(ROOT_DIR, 'data', 'airports.csv')
RUNWAYS_FILE = os.path.join(ROOT_DIR, 'data', 'runways.csv')

re_clean_airport = re.compile(
    r'(airport|air base|air force base|international)', re.I)


def clean_name(airport_name):
    return ' '.join(re_clean_airport.sub('', airport_name).split())


class Runway(object):

    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width

    def __repr__(self):
        return '<Runway: %s (%dm/%dm)>' % (self.name, self.length, self.width)


class Airport(object):

    def __init__(self, id, icao, name, lat, lon):
        self.id = id
        self.icao = icao
        self.name = name
        self.lat = lat
        self.lon = lon
        self.runways = []

    def __repr__(self):
        return '<Airport: %s (%s)>' % (self.icao, self.name)


def parse_airports():
    runways = {}
    with open(RUNWAYS_FILE, 'r') as fp:
        for line in DictReader(fp):
            ref = line['airport_ref']
            rwys = runways.setdefault(ref, [])
            rwys.append(line)

    rv = OrderedDict()
    with open(AIRPORTS_FILE, 'r') as fp:
        for line in DictReader(fp):
            if not line['gps_code']:
                continue
            if not line['type'].endswith('_airport'):
                continue
            apt = Airport(line['id'],
                          line['gps_code'],
                          clean_name(line['name']),
                          float(line['latitude_deg']),
                          float(line['longitude_deg']))
            for l in runways.get(apt.id, []):
                if l['le_ident']:
                    rwy = Runway(l['le_ident'],
                                 ft2m(l['length_ft']),
                                 ft2m(l['width_ft']))
                    apt.runways.append(rwy)
                if l['he_ident']:
                    rwy = Runway(l['he_ident'],
                                 ft2m(l['length_ft']),
                                 ft2m(l['width_ft']))
                    apt.runways.append(rwy)

            rv[line['gps_code']] = apt

    return rv
