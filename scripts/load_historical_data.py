from models import HistoricalTrainPosition
import datetime
import json

import os
import os.path
PATH = "/home/fwilson/Downloads/new/metrologging/rail"

print("starting")

filenames = list(os.path.join(PATH, i) for i in os.listdir(PATH))
for filename in filenames:
    data = json.load(open(filename))["Trains"]
    for train in data:
        next_station = train["LocationCode"]
        dest_station = train["DestinationCode"]
        line_code = train["Line"]

        if dest_station is None or next_station is None or line_code == "No" or train["Car"] is None:
            continue

        cars = int(train["Car"]) if train["Car"] != "-" else 6
        cars = 8 if cars == 2 else cars

        if train["Min"].isnumeric():
            time = int(train["Min"])

        else:
            if "-" in train["Min"]:
                continue
            time = 1 if train["Min"] == "ARR" else 0

        ts = datetime.datetime.fromtimestamp(int(float(filename.split("/")[-1])))

        HistoricalTrainPosition.create(cars=cars, line_code=line_code, time=time,
                                       next_station=next_station, dest_station=dest_station,
                                       timestamp=ts)
