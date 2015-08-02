from models import HistoricalTrainPosition

pos = list(HistoricalTrainPosition.select())
dels = []
for p in pos:
    if p.timestamp.microsecond == 0:
        dels.append(p.id)

print(HistoricalTrainPosition.delete().where(HistoricalTrainPosition.id << dels).execute())
