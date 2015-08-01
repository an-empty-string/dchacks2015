import requests
from time import time
from ..config import config

APIKEY=config["API_KEY"]
s = requests.get("https://api.wmata.com/Incidents.svc/json/Incidents?api_key={}".format(APIKEY))
open("rail_incidents/{}".format(time()), "w").write(s.text)

t = requests.get("https://api.wmata.com/Incidents.svc/json/ElevatorIncidents?api_key={}".format(APIKEY))
open("rail_outages/{}".format(time()), "w").write(t.text)

u = requests.get("https://api.wmata.com/Incidents.svc/json/BusIncidents?api_key={}".format(APIKEY))
open("bus_incidents/{}".format(time()), "w").write(u.text)
