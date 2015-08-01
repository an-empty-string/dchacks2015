from peewee import *
from config import db

class BaseModel(Model):
    class Meta:
        database = db

class HistoricalTrainPosition(BaseModel):
    cars = IntegerField()
    line_code = CharField()
    next_station = CharField()
    dest_station = CharField()
    time = IntegerField()
    timestamp = DateTimeField()
