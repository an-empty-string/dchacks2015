__author__ = 'claudia'
from config import wmata
import csv
csvdata = []
with open('stops.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for x in reader:
        csvdata.append(float(x[5]),float(x[6]),1/30)
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
with open("data2.csv", "w") as f:
    f.write(stringydata)
print("Done")