__author__ = 'claudia'
from config import wmata
import json
data = {
    "metrobus": [],
    "metrorail": []
}

for line in wmata.lines.all:
    for staa in wmata.lines[line].stations:
        if line == 'RD':
            headway = 4.5
        elif line == 'BL':
            headway = 12
        else:
            headway = 6
        data["metrorail"].append({
            "lat": staa.location.lat,
            "lon": staa.location.lon,
            "headway": headway,
            "weight": 10/headway,
            "line": line,
            "name": staa.name,
            "station_code": staa.station_code
        })

bus_stops = json.loads(open("bus-stops.json", "r").read())
bus_stops = bus_stops["Stops"]
for stop in bus_stops:
    data["metrobus"].append({
        "lat": float(stop["Lat"]),
        "lon": float(stop["Lon"]),
        "weight": len(stop["Routes"])/20,
        "routes": stop["Routes"],
        "name": stop["Name"],
        "stop_id": stop["StopID"]
    })

jsonexp = json.dumps(data)
print("Converted")
with open("gen/export.json", "w") as f:
    f.write(jsonexp)
with open("export.json", "w") as f:
    f.write(jsonexp)
print("Done")