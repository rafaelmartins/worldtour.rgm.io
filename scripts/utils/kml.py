# coding: utf-8


def render_kml_airport(airports):
    rv = '''\
<?xml version="1.0" encoding="utf-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
'''
    for airport in airports:
        rv += (
            '    <Placemark><name>%s - %s</name><Point>'
            '<coordinates>%f,%f,0</coordinates></Point></Placemark>\n'
        ) % (airport.icao, airport.name, airport.lon, airport.lat)

    rv += '''\
  </Document>
</kml>'''
    return rv


def render_kml_route(airports):
    rv = '''\
<?xml version="1.0" encoding="utf-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
'''

    origin = None
    for airport in airports:
        if origin is not None:
            rv += (
                '    <Placemark><name>%s -> %s</name><LineString>'
                '<coordinates>%f,%f,0 %f,%f,0</coordinates></LineString>'
                '</Placemark>\n'
            ) % (origin.icao, airport.icao, origin.lon, origin.lat,
                 airport.lon, airport.lat)
        rv += (
            '    <Placemark><name>%s - %s</name><Point>'
            '<coordinates>%f,%f,0</coordinates></Point></Placemark>\n'
        ) % (airport.icao, airport.name, airport.lon, airport.lat)
        origin = airport

    rv += '''\
  </Document>
</kml>'''
    return rv
