__author__ = 'claudia'
from config import wmata
import json
csvdata = []
bus_stops = json.loads(open("bus-stops.json", "r").read())
bus_stops = bus_stops["Stops"]
for stop in bus_stops:
    csvdata.append([
        float(stop["Lat"]),
        float(stop["Lon"]),
        len(stop["Routes"])/10
    ])
for s in wmata.lines.all:
    for staa in wmata.lines[s].stations:
        if s == 'RD':
            headway = 4.5
        elif s == 'BL':
            headway = 12
        else:
            headway = 6
        csvdata.append((staa.location.lat, staa.location.lon, 5/headway))

stringydata = "\n".join([",".join(list(map(str, i))) for i in csvdata])
print("Converted")
with open("gen/data2.csv", "w") as f:
    f.write(stringydata)
with open("data2.csv", "w") as f:
    f.write(stringydata)
print("Done")