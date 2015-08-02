from flask import jsonify
from models import CurrentTrainPosition
from config import wmata

def _station_fmt(station):
    return {
        "name": station.name,
        "station_code": station.station_code
    }

def _station_fmt_complete(station):
    return {
        "name": station.name,
        "station_code": station.station_code,
        "lat": station.location.lat,
        "lon": station.location.lon,
        "lines": [k.line_code for k in station.lines]
    }

def _line_fmt(line):
    return {
        "friendly_name": line.friendly_name,
        "line_code": line.line_code
    }

def _line_fmt_complete(line):
    return {
        "friendly_name": line.friendly_name,
        "line_code": line.line_code,
        "stations": [k.station_code for k in line.stations]
    }

def _line_fmt_stations(line):
    return {
        "friendly_name": line.friendly_name,
        "line_code": line.line_code,
        "stations": [_station_fmt_complete(wmata.stations[k.station_code]) for k in line.stations]
    }


def get_all_trains():
    print("Loading all predictions")
    predictions = wmata.rail_system.predictions()
    print("Done")
    output = []
    for tr in predictions:
        output.append({
            "destination": _station_fmt(tr.destination),
            "station": _station_fmt(tr.station),
            "cars": tr.cars,
            "line": _line_fmt(tr.line),
            "time": tr.time,
            "time_int": tr.time_int
        })
    return jsonify(predictions=output)

def get_trains_on_line(line):
    print("Loading predictions for line")
    predictions = wmata.rail_system.predictions()
    print("Done")
    output = []
    for tr in predictions:
        if tr.line.line_code == line:
            output.append({
                "destination": _station_fmt(tr.destination),
                "station": _station_fmt(tr.station),
                "cars": tr.cars,
                "line": _line_fmt(tr.line),
                "time": tr.time,
                "time_int": tr.time_int
            })
    return jsonify(predictions=output)

def get_trains_at_station(station_code):
    print("getting trains at station")
    output = []
    if station_code in wmata.stations.all:
        print("Loading predictions")
        station = wmata.stations[station_code]
        trains = station.trains()
        print("Done")
        for tr in trains:
            output.append({
                "destination": _station_fmt(tr.destination),
                "station": _station_fmt(tr.station),
                "cars": tr.cars,
                "line": _line_fmt(tr.line),
                "time": tr.time,
                "time_int": tr.time_int
            })
    return jsonify(predictions=output)

def get_station_by_code(code):
    station = wmata.stations[code]
    return jsonify(_station_fmt_complete(station))

def get_line_by_code(code):
    line = wmata.lines[code]
    return jsonify(_line_fmt_complete(line))

def get_stations():
    return jsonify(stations=[_station_fmt_complete(i) for i in wmata.stations.all.values()])

def get_lines():
    return jsonify(lines=[_line_fmt_complete(i) for i in wmata.lines.all.values()])

def get_lines_full():
    return jsonify(lines=[_line_fmt_stations(i) for i in wmata.lines.all.values()])

def client_grab():
    return jsonify(
        lines=[_line_fmt_stations(i) for i in wmata.lines.all.values()],
        stations=[_station_fmt_complete(i) for i in wmata.stations.all.values()]
    )


def get_train_positions():
    trains = list(CurrentTrainPosition.select())
    data = []
    for i in trains:
        data.append(dict(near=_station_fmt(wmata.stations[i.station_near]),
                         far=_station_fmt(wmata.stations[i.station_far]),
                         fraction=i.fraction))
    return jsonify(data=data)
