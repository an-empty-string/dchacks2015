from flask import send_from_directory
from . import app
from .views import api, main

routes = (
    ('/api/trains/', api.get_all_trains),
    ('/api/trains/line/<line>/', api.get_trains_on_line),
    ('/api/trains/station/<station_code>/', api.get_trains_at_station),
    ('/', main.index)
)

@app.route('/gen/<path:path>')
def staticfiles(path):
    return send_from_directory('gen', path)

for route, endpoint in routes:
    app.add_url_rule(route, endpoint.__name__, endpoint)
