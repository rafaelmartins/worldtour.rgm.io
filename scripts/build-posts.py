#!/usr/bin/env python2
# coding: utf-8

import codecs
import collections
import os

import jinja2

from utils.ourairports import parse_airports

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTE_FILE = os.path.join(ROOT_DIR, 'data', 'route.txt')
FLIGHT_DIR = os.path.join(ROOT_DIR, 'content', 'flight')

TEMPLATE = jinja2.Template(u'''\
TITLE: Flight {{ flight }}: {{ departure }} ({{ departure_icao }}) → \
{{ arrival }} ({{ arrival_icao }})
DATE:
-------------------------
#### Flight details

- **Flight**: MAG{{ "%04d"|format(flight) }}
- **Departure**: {{ departure }} ({{ departure_icao }})
- **Arrival**: {{ arrival }} ({{ arrival_icao }})
- [**ACARS Log**]()

#### Full flight

<iframe
    src="https://www.youtube.com/embed/"
    width="560"
    height="315"
    frameborder="0"
    style="border: 0"
    allowfullscreen>
</iframe>

#### Take-off and landing

<iframe
    src="https://www.youtube.com/embed/"
    width="560"
    height="315"
    frameborder="0"
    style="border: 0"
    allowfullscreen>
</iframe>

''')


def build_flight(airports, index, origin, destination):
    print 'building %s -> %s' % (origin, destination)
    if not os.path.exists(FLIGHT_DIR):
        os.makedirs(FLIGHT_DIR)
    fname = os.path.join(FLIGHT_DIR, '%s-%s.txt' % (origin, destination))
    o = airports[origin]
    d = airports[destination]
    with codecs.open(fname, 'w', 'utf-8') as fp:
        fp.write(TEMPLATE.render(flight=index,
                                 departure=o.name.decode('utf-8'),
                                 departure_icao=origin.decode('utf-8'),
                                 arrival=d.name.decode('utf-8'),
                                 arrival_icao=destination.decode('utf-8')))


def main():
    airports = parse_airports()

    with open(ROUTE_FILE) as fp:
        origin = None
        index = 0
        for destination in fp.read().split():
            if origin is not None:
                index += 1
                build_flight(airports, index, origin, destination)
            origin = destination


if __name__ == '__main__':
    main()
