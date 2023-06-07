from flask import Flask, request
from flask_cors import CORS, cross_origin
from query import search_fooddb

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/get_food_matches", methods=['POST'])
@cross_origin(supports_credentials=True)
def get_food_matches():
    if request.method == 'POST':
        menu_items = request.data
        food_matches = search_fooddb(menu_items, .4)
    return food_matches
