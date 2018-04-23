# Scripts

## `build-posts.py`

Generates blog posts for all the flights, from a template. Reads flights
from `../data/route.txt`.

## `download-ourairports.sh`

Downloads CSV data files from ouairports.com, with airports and runways data.
Must be run before running any of the Python scripts for the first time.

## `download-scenery.py`

Downloads scenery files from X-Plane Gateway. It will download any scenery
that is required for the World Tour and was updated after the last X-Plane
release.

## `map-elegible.py`

Builds a KML with the airports elegible for the World Tour.

## `map-route.py`

Builds a KML with the airports and routes for the World Tour, from
`../data/route.txt`.

## `scripts/`

Helper library with most of the actual implementation.
