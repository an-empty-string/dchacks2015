from config import wmata

lines = list(wmata.lines.all.values())

times = {}
times_lists = {}

for line in lines:
    print(line.friendly_name)
    times_lists[line.line_code] = [0]
    end_station = line.stations[0]
    other_stations = line.stations[1:]
    for other_station in other_stations:
        times_lists[line.line_code].append(end_station.route_meta(other_station).time)

    for idx1, station1 in enumerate(line.stations):
        if station1 not in times:
            times[station1] = {}
        for idx2, station2 in enumerate(line.stations):
            times[station1][station2] = abs(times_lists[line.line_code][idx1] - times_lists[line.line_code][idx2])

trains = wmata.rail_system.predictions()

import pprint
pprint.pprint(times)
