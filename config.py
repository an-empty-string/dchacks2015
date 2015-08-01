import json
import utils.metro
from peewee import *

with open("config.json") as f:
    config = json.load(f)

redis_info = {"host": config["REDIS_HOST"], "password": config["REDIS_PASSWORD"]}
wmata = utils.metro.MetroApi(config["API_KEY"], redis_info)

db = PostgresqlDatabase(config["POSTGRES_USER"], host=config["POSTGRES_HOST"],
                        user=config["POSTGRES_USER"],
                        password=config["POSTGRES_PASSWORD"])
