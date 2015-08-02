from . import app
from .views import basic

routes = (
    ('/api/trains/', basic.get_all_trains),
    ('/api/trains/line/<line>/', basic.get_trains_on_line),
    ('/api/trains/station/<station_code>/', basic.get_trains_at_station)
)

for route, endpoint in routes:
    app.add_url_rule(route, endpoint.__name__, endpoint)
