from flask import send_from_directory
from . import app
from .views import api, main

routes = (
    ('/api/trains/', api.get_all_trains),
    ('/api/trains/line/<line>/', api.get_trains_on_line),
    ('/api/trains/station/<station_code>/', api.get_trains_at_station),
    ('/api/station/<code>/', api.get_station_by_code),
    ('/api/stations/', api.get_stations),
    ('/api/lines/', api.get_lines),
    ('/api/trainpos/', api.get_train_positions),
    ('/', main.index)
)

@app.route('/gen/<path:path>')
def genfiles(path):
    return send_from_directory('gen', path)

@app.route('/static/<path:path>')
def genstatic(path):
    return send_from_directory('static', path)

for route, endpoint in routes:
    app.add_url_rule(route, endpoint.__name__, endpoint)
