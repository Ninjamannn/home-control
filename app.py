import falcon

import handlers
import middlewares


app = falcon.API(middleware=[
    middlewares.TokenAuthMiddleware(),
])


# handlers
app.add_route(
    '/rooms/sensors',
    handlers.SensorDataHandler(),
)
