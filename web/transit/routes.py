import transit
import transit.views.basic

from transit import app

routes = (
    ('/api/trains/', transit.views.basic.get_all_trains),
    ('/api/trains/line/<line>/', transit.views.basic.get_trains_on_line),
    ('/api/trains/station/<station>/', transit.views.basic.get_trains_at_station)
)

for route, func in routes:
    app.add_url_rule(rule=route, endpoint.__name__, endpoint)
