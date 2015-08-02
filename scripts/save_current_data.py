from models import HistoricalTrainPosition
from config import wmata
from datetime import datetime
import json

import os
import os.path


all_trains = wmata.rail_system.predictions()


ts = datetime.now()

for train in all_trains:
    next_station = train.station.station_code
    dest_station = train.destination.station_code
    line_code = train.line.line_code

    cars = train.cars
    time = train.time_int
    group = train.group

    HistoricalTrainPosition.create(cars=cars, line_code=line_code, time=time, group=group,
                                   next_station=next_station, dest_station=dest_station,
                                   timestamp=ts)


print("Added", len(all_trains), "trains at", ts)