import requests
import json
from time import time,sleep

from ..config import config

APIKEY=config["API_KEY"]
def l(route):
    r = requests.get("https://api.wmata.com/Bus.svc/json/jRouteSchedule?routeID={}&api_key={}".format(route, APIKEY))
    open("bus_route/{}".format(route), "w").write(r.text)

routes = json.loads(open("bus-routes.txt").read())
routes = routes["Routes"]
for r in routes:
    print(r)
    l(r["RouteID"])
    sleep(3.5)
