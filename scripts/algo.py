__author__ = 'claudia'
from config import wmata
from math import hypot

def finddist(stat, lata, longa):
    dx = stat.location.lon - longa
    dy = stat.location.lat - lata
    return hypot(dx,dy)

def findadd(stat, lata, longa):
    wa = finddist(stat, lata, longa)
    const = 1
    return const/(wa**2)

def pointcalc(lata,longa):
    i = 0.0
    for s in wmata.lines:
        for stat in s:
             
