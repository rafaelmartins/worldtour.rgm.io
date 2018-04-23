# coding: utf-8

from base64 import b64decode
from cStringIO import StringIO

import requests
import zipfile

# I have the following custom sceneries installed
SCENERY_WHITELIST = [

    # payware
    'EDDF',
    'EDDT',
    'EHAM',
    'BIKF',
    'LOWI',
    'TFFJ',

    # default from x-plane custom scenery (good?)
    'EDLP',
    'EGLL',
    'LFMN',
    'LFPO',
    'LFPR',
    'LOWI',
]

session = requests.Session()
sceneries = None


def get_xp11_sceneries():
    r = session.get('http://gateway.x-plane.com/apiv1/releases')
    if r.status_code == 404:
        return None
    r.raise_for_status()
    latest = None
    for release in r.json()[::-1]:
        if release['Version'].startswith('11.'):
            if latest is None:
                latest = release.copy()
            elif latest['Date'] < release['Date']:
                latest = release.copy()
    if latest is None:
        return None

    r = session.get('http://gateway.x-plane.com/apiv1/release/%s' %
                    latest['Version'])
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()['SceneryPacks']


def get_scenery_id(icao):
    r = session.get('https://gateway.x-plane.com/apiv1/airport/%s' % icao)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    for scenery in r.json().get('airport', {}).get('scenery', [])[::-1]:
        if scenery['type'] == u'3D' and scenery['Status'] == 'Approved':
            return scenery['sceneryId']


def get_apt_dat(id):
    r = session.get('https://gateway.x-plane.com/apiv1/scenery/%d' % id)
    if r.status_code == 404:
        return False
    r.raise_for_status()
    zip_content = r.json().get('scenery', {}).get('masterZipBlob')
    if not zip_content:
        return None
    with zipfile.ZipFile(StringIO(b64decode(zip_content))) as zip:
        for f in zip.infolist():
            if f.filename.endswith('.dat'):
                return zip.read(f.filename)


def has_scenery(icao):
    if icao in SCENERY_WHITELIST:
        return True
    id = get_scenery_id(icao)
    if id is None:
        return False
    dat = get_apt_dat(id)
    if dat is None:
        return False
    for l in dat.splitlines():
        if l.startswith('1300 ') and 'jets' in l.split()[5].split('|'):
            return True
        if l.startswith('15 '):  # there's no way to validate gate type
            return True
    return False
