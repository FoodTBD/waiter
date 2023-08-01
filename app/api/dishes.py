import datetime

import flask
from connexion import NoContent

data = {}

def post(body):
    new_id = f'dish_{len(data)+1}'

    new_obj = body
    new_obj['id'] = new_id
    new_obj['dateCreated'] = datetime.datetime.now()

    data[new_id] = new_obj

    headers = {}
    headers['Location'] = flask.url_for('api_dishes_get', dishId=new_id)

    return NoContent, 201, headers


def search(limit=100):
    return list(data.values())[0:limit], 200


def get(dishId):
    obj = data.get(dishId)
    if not obj:
        return NoContent, 404

    # Inject displayXXX properties, derived from from localizedXXX
    for property_stem in ['Name', 'Title', 'Description', 'WikipediaUrl']:
        localized_map = obj.get(f'localized{property_stem}s', {})
        for key in localized_map.keys():
            if key.startswith('en'):
                obj[f'display{property_stem}'] = localized_map[key]
                break

    return obj

def put(dishId):
    pass

def delete(dishId):
    pass
