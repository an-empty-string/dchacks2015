from models import HistoricalTrainPosition
from config import wmata
from datetime import datetime
import json

import os
import os.path

pos = list(HistoricalTrainPosition.select())
updates = 0

for tr in pos:

    trackgroup = tr.trackgroup

    if trackgroup is not None:
        continue

    """LEFT side of Metro map = 2 (incl Branch Ave)
       RIGHT side of Metro map = 1 (incl Greenbelt)
    """
                        #ShGrv, Wihle, Vnna, FrncSp, Hntgn, BchAv 
    if dest_station in ['A15', 'N06', 'K08', 'J03', 'C15', 'F11']:
        trackgroup2.append(tr.id)
                          #Glnmt, Grnblt, NCrl, Lrgo, Grnbt, MtVrn, FtTtn, FtTtn
    elif dest_station in ['B11', 'E10', 'D13', 'G05', 'F11', 'E01', 'B06', 'E06']:
        trackgroup1.append(tr.id)

    if trackgroup is None:
        continue
    updates += 1


print(updates, "updates")