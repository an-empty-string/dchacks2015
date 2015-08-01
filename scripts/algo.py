__author__ = 'claudia'
from config import wmata
from math import hypot


def find_dist(stat, lata, longa):
    dx = stat.location.lon - longa
    dy = stat.location.lat - lata
    return hypot(dx,dy)


def find_add(stat, lata, longa):
    wa = find_dist(stat, lata, longa)
    const = 1  # fix this later- this is what you need to solve!!!
    return const/(wa**2)


def point_calc(lata, longa):
    i = 0.0
    for s in wmata.lines:
        for staa in s:
            i += find_add(staa, lata, longa)
    return i


def point_map(start_lat, stop_lat, start_lon, stop_lon, resolution):
    latlist = list(f_range(start_lat, stop_lat, resolution))
    lonlist = list(f_range(start_lon, stop_lon, resolution))
    return {lat: {lon: point_calc(lat, lon) for lon in lonlist} for lat in latlist}


def f_range(mini, maxi, step):
    while mini < maxi:
        yield mini
        mini += step
