import datetime

import flask
from connexion import NoContent

data = {}

def post(body):
    new_id = f'place_{len(data)+1}'

    new_obj = body
    new_obj['id'] = new_id
    new_obj['dateCreated'] = datetime.datetime.now()

    data[new_id] = new_obj

    headers = {}
    headers['Location'] = flask.url_for('api_places_get', placeId=new_id)

    return NoContent, 201, headers


def search(limit=100):
    return list(data.values())[0:limit], 200


def get(placeId):
    obj = data.get(placeId)
    if not obj:
        return NoContent, 404
    return obj
