__author__ = 'claudia'
from config import wmata

csvdata = []
for s in wmata.lines.all:
    for staa in wmata.lines[s].stations:
        if s == 'RD':
            headway = 4.5
        elif s == 'BL':
            headway = 12
        else:
            headway = 6
        csvdata.append((staa.location.lat, staa.location.lon, 1/headway))
stringydata = "\n".join([",".join(list(map(str, i))) for i in csvdata])
with open("data2.csv", "w") as f:
    f.write(stringydata)
print("Done")