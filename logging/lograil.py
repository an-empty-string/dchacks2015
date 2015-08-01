import requests
from time import time
from ..config import config

APIKEY=config["API_KEY"]
r = requests.get("https://api.wmata.com/StationPrediction.svc/json/GetPrediction/All?api_key={}".format(APIKEY))
open("rail/{}".format(time()), "w").write(r.text)

v = requests.get("https://api.wmata.com/Bus.svc/json/jBusPositions?api_key={}".format(APIKEY))
open("bus_positions/{}".format(time()), "w").write(v.text)
