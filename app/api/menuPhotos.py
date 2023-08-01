import datetime

import flask
from connexion import NoContent

data = {}

def search(limit=100):
    return list(data.values())[0:limit], 200

def get(menuId):
    obj = data.get(menuId)
    if not obj:
        return NoContent, 404
    return obj

def post(body):
    pass

def delete(menuId):
    pass
