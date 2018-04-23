#!/usr/bin/env python2
# coding: utf-8

from utils.xplane import get_scenery_id, get_xp11_sceneries

import os
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTE_FILE = os.path.join(ROOT_DIR, 'data', 'route.txt')
SCENERY_DIR = os.path.join(ROOT_DIR, 'scenery')


def main():
    xp11 = get_xp11_sceneries()

    with open(ROUTE_FILE) as fp:
        route_list = fp.read().split()

    for icao in route_list:
        sc_id = get_scenery_id(icao)
        if not sc_id:
            continue

        if sc_id not in xp11:
            subprocess.check_call([
                'wget',
                '--content-disposition',
                '-P', SCENERY_DIR,
                '-c',
                'https://gateway.x-plane.com/scenery/download/%d' % sc_id
            ])


if __name__ == '__main__':
    main()
