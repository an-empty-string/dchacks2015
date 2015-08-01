import json
import utils.metro

with open("config.json") as f:
    config = json.load(f)

redis_info = {"host": config["REDIS_HOST"], "password": config["REDIS_PASSWORD"]}
wmata = utils.metro.MetroApi(config["API_KEY"], redis_info)
