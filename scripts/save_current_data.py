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
    try:
        trackgroup = int(train.group)
    except ValueError:
        """LEFT side of Metro map = 2 (incl Branch Ave)
           RIGHT side of Metro map = 1 (incl Greenbelt)
        """
                            #ShGrv, Wihle, Vnna, FrncSp, Hntgn, BchAv 
        if dest_station in ['A15', 'N06', 'K08', 'J03', 'C15', 'F11']:
            trackgroup = 2
                              #Glnmt, Grnblt, NCrl, Lrgo, Grnbt, MtVrn, FtTtn, FtTtn
        elif dest_station in ['B11', 'E10', 'D13', 'G05', 'F11', 'E01', 'B06', 'E06']:
            trackgroup = 1

    HistoricalTrainPosition.create(cars=cars, line_code=line_code, time=time, trackgroup=track_group,
                                   next_station=next_station, dest_station=dest_station,
                                   timestamp=ts)


print("Added", len(all_trains), "trains at", ts)