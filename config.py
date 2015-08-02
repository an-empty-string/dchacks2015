import json
import utils.metro

with open("config.json") as f:
    config = json.load(f)

redis_info = {"host": config["REDIS_HOST"], "password": config["REDIS_PASSWORD"]}
print("Connecting to WMATA API redis server...")
wmata = utils.metro.MetroApi(config["API_KEY"], redis_info=redis_info)
print("Connected.")
