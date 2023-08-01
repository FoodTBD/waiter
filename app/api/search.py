import datetime

import flask
from connexion import NoContent

data = {}

def search(limit=100):
    return list(data.values())[0:limit], 200
