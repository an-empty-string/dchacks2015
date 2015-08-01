from models import HistoricalTrainPosition
from config import wmata
from datetime import datetime
import json

import os
import os.path


all_trains = wmata.rail_system.predictions()

for train in all_trains:
    next_station = train.station.station_code
    dest_station = train.destination.station_code
    line_code = train.line.line_code

    cars = train.cars
    time = train.time_int

    ts = datetime.now()

    print(next_station, time, line_code, dest_station, cars)

    HistoricalTrainPosition.create(cars=cars, line_code=line_code, time=time,
                                   next_station=next_station, dest_station=dest_station,
                                   timestamp=ts)