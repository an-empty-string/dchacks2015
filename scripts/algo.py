__author__ = 'claudia'
from config import wmata
from math import hypot


def find_dist(stat, lata, longa):
    dx = stat.location.lon - longa
    dy = stat.location.lat - lata
    return hypot(dx,dy)


def find_add(line, stat, lata, longa):
    wa = find_dist(stat, lata, longa)
    const = 1 / calc_trainfreq(line)
    return const/(wa**2)


def point_calc(lata, longa):
    i = 0.0
    for s in wmata.lines:
        for staa in s:
            i += find_add(s, staa, lata, longa)
    return i


def point_map(start_lat, stop_lat, start_lon, stop_lon, resolution):
    latlist = list(f_range(start_lat, stop_lat, resolution))
    lonlist = list(f_range(start_lon, stop_lon, resolution))
    return {lat: {lon: point_calc(lat, lon) for lon in lonlist} for lat in latlist}


def f_range(mini, maxi, step):
    while mini < maxi:
        yield mini
        mini += step


def calc_trainfreq(m):
    return 0


def samplerunfullcity():
    point_map(38.755377, 39.130282, -77.314407, -76.829635, .001)
    print("Done")

if __name__ == '__main__':
    samplerunfullcity()