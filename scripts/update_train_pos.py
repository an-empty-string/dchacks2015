from config import wmata
from datetime import datetime
from models import CurrentTrainPosition, db
from ipdb import launch_ipdb_on_exception

with launch_ipdb_on_exception():
    ts = datetime.strptime("2015-07-29 08:04:58", "%Y-%m-%d %H:%M:%S")
    # wmata.timestamp = ts

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
    print("got {} predictions".format(len(trains)))
    d = []

    for train in trains:
        train.time_to_dest = train.time_int + times[train.direction_dest][train.station]
        dkey = (train.time_to_dest, train.line.line_code, train.direction_dest.station_code)
        for i in d:
            if i.line == train.line and train.direction_dest == i.direction_dest:
                if abs(times[i.direction_dest][train.station] + i.time_int - train.time_to_dest) < 2:
                    break
        else:
            d.append(train)

    print("now have {} trains".format(len(d)))
    trains = d

    ds = []

    for train in trains:
        time = times[train.direction_dest][train.station] + train.time_int
        stations_on_line = train.line.stations
        if stations_on_line[0] != train.direction_dest:
            stations_on_line.reverse()
        try:
            stations = list(zip(stations_on_line, [times[train.direction_dest][station] for station in stations_on_line]))
        except:
            continue
        for station, time_from_end in stations:
            if time_from_end > time:
                station_far = station
                break
        else:
            continue
        station_near = stations[[i[0] for i in stations].index(station_far) - 1][0]
        fraction = 1 - ((times[train.direction_dest][station_far] - time) / times[station_near][station_far])
        ds.append(dict(fraction=fraction, station_near=station_near.station_code, station_far=station_far.station_code))
        print("{}% between {} and {}".format(round(fraction * 100, 1), station_near, station_far))

    with db.atomic():
        CurrentTrainPosition.delete()
        CurrentTrainPosition.insert_many(ds).execute()

    import pprint
    # pprint.pprint(times)
