__author__ = 'claudia'
from config import wmata
from math import hypot


def find_dist(stat, lata, longa):
    dx = stat.location.lon - longa
    dy = stat.location.lat - lata
    return hypot(dx,dy)


def find_add(stat, lata, longa):
    wa = find_dist(stat, lata, longa)
    const = 1
    return const/(wa**2)


def point_calc(lata,longa):
    i = 0.0
    for s in wmata.lines:
        for staa in s:
            i += find_add(staa, lata, longa)
    return i

