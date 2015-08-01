import json
import utils.metro
with f as open("config.json"):
    config = json.load(f)

redis_info = {"host": config["REDIS_HOST"], "password": config["REDIS_PASSWORD"]}
wmata = utils.metro.MetroApi(config["API_KEY"], **redis_info)
