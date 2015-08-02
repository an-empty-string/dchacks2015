from flask import jsonify
from config import wmata


def _station_fmt(station):
    return {
        "name": station.name,
        "station_code": station.station_code
    }

def _line_fmt(line):
    return {
        "friendly_name": line.friendly_name,
        "line_code": line.line_code
    }

def get_all_trains():
    print("Loading predictions..")
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
    print("Loading predictions")
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
    print("Loading predictions")
    predictions = wmata.rail_system.all_trains()
    print("Done")
    output = []
    if station_code in wmata.stations:
        station = wmata.stations[line_code]

        if station in predictions:
            trains = predictions[station]
    
            for tr in trains:
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

