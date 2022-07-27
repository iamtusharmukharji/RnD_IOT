from flask_cors import CORS, cross_origin
from IotApp import app


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from . import client_routes, device_routes