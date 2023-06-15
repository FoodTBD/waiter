import json

from flask import Flask, request
from flask_cors import CORS, cross_origin
from ocr import get_easyocr_results
from query import search_algolia, search_fooddb
import re

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/get_food_matches_from_string", methods=['POST'])
@cross_origin(supports_credentials=True)
def get_food_matches_from_string():
    """
    Receives an easyocr results array, parses and performs a search of the db
    :return: a list of possible food matches
    """
    if request.method == 'POST':
        req_data = json.loads(request.data)
        menu_str = req_data['searchText']
        levenshtein_ratio = float(req_data['levenshteinRatio'])
        # parse menu string
        items = re.split('\((.*?)\)', menu_str)
        del items[0] # remove '['
        del items[-1]# remove ']\n'
        items = [x for x in items if not x.strip() == ','] # remove extra commas
        menu_items = []
        # recreate tuples
        for i in items:
            ocr_list = re.split('\[(.*?)\]', i)
            # get the name of the food and the confidence level
            ocr_list_split_1 = ocr_list.pop(-1).split(',')
            conf_level = float(ocr_list_split_1.pop().strip())
            food_name = ocr_list_split_1.pop().strip().replace("'", "")
            # clean for bounding box
            bounding_box_list = []
            bounding_box_str_list= [x for x in ocr_list if not x.strip() == ','] # remove extra commas
            bounding_box_str_list = [x for x in bounding_box_str_list if not x.strip() == '']  # remove empty spaces
            for b in bounding_box_str_list:
                b = b.replace('[', '').replace(']', '')
                box_coords_str_list = b.split(',')
                bounding_box_list.append([float(box_coords_str_list[0].strip()), float(box_coords_str_list[1].strip())])
            menu_items.append((bounding_box_list, food_name, conf_level))
        # food_matches = search_fooddb(menu_items, levenshtein_ratio)
        food_matches = search_algolia(menu_items)
        print(f'Found {len(food_matches)} matches')
    return json.dumps({'matches': food_matches})

@app.route("/get_food_matches_from_image", methods=['POST'])
@cross_origin(supports_credentials=True)
def get_food_matches_from_image():
    """
    Receives the image file and the desired lists of translation languages, runs the image through the
    ocr and then finds the food matches
    :return: list of food matches
    """
    if request.method == 'POST':
        image = request.files['file']
        image_path = './snapshots/' + image.filename
        # save image to local snapshots directory for easy ocr
        image.save(image_path)
        lang_list = request.form['lang_list'].replace(' ', '').split(',')
        print('Running {image.filename} through EasyOCR')
        menu_items = get_easyocr_results(image_path, lang_list)
        print('Searching DB...')
        food_matches = search_fooddb(menu_items, .4)
    return food_matches
