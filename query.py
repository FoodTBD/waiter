#!/usr/bin/env python

import csv
import Levenshtein
import re
from algoliasearch.search_client import SearchClient
from algolia_api_keys import ALGOLIA_SEARCH_API_KEY, EATS_DB_INDEX

# For testing
MENU_ITEMS = [([[3, 1], [132, 1], [132, 44], [3, 44]], '芥蘭炒雞鬆', 0.9925057535175006), ([[160, 0], [589, 0], [589, 34], [160, 34]], 'Sauteed Chinese broccoli & chicken', 0.6650856223897282), ([[612, 0], [705, 0], [705, 36], [612, 36]], '$14.95', 0.9966048137234976), ([[3, 39], [84, 39], [84, 80], [3, 80]], '宮保雞', 0.9938148107521922), ([[160, 35], [391, 35], [391, 71], [160, 71]], 'Kung pao chicken', 0.9950338080918358), ([[616, 36], [704, 36], [704, 66], [616, 66]], '$14.95', 0.678551353406021), ([[3, 74], [108, 74], [108, 114], [3, 114]], '金沙南瓜', 0.9979552030563354), ([[162, 71], [446, 71], [446, 104], [162, 104]], 'Pumpkin wisalted egg', 0.5931087250353343), ([[617, 69], [706, 69], [706, 102], [617, 102]], '$13.95', 0.9994072939294798), ([[3, 107], [134, 107], [134, 149], [3, 149]], '魚香茄子煲', 0.9960084943703202), ([[162, 103], [579, 103], [579, 144], [162, 144]], 'Eggplant in garlic sauce clay pot', 0.9856214430154885), ([[618, 106], [708, 106], [708, 136], [618, 136]], '$14.95', 0.999465799060174), ([[3, 135], [574, 135], [574, 185], [3, 185]], 'X0醬豆仔炒茄子 Sauteed eggplant & string beans', 0.6587818191850608), ([[620, 140], [710, 140], [710, 170], [620, 170]], '$14.95', 0.9874156124127652), ([[163, 168], [312, 168], [312, 198], [163, 198]], 'W/XO sauce', 0.3475397741897711), ([[444.5430712064641, 73.37752817163539], [503.5549749501136, 67.42770772300699], [505.4569287935359, 96.62247182836461], [446.4450250498864, 102.57229227699301]], 'yolk', 0.9997640252113342)]
# MENU_ITEMS = [([[3, 39], [84, 39], [84, 80], [3, 80]], '불고기', 0.9938148107521922),
#               ([[160, 0], [589, 0], [589, 34], [160, 34]], 'Sпельмени', 0.6650856223897282)]
def get_fooddb():
    """
    Test function to retrieve current db from csv
    :return:
    """
    file_name = './EatsDB.csv'
    with open(file_name, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        foods = []
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            foods.append(row)
            line_count += 1
        print(f'Processed {line_count} lines.')
    return foods

def search_fooddb(menu_items, min_levenshtein_ratio):
    """
    Search food items dict for requested menu items

    Uses Levenshtein ratio to determine string matching
    :param menu_items:
    :param min_levenshtein_ratio
    :return:
    """
    food_db = get_fooddb()
    match_list = []

    for item in menu_items:
        food_item_matches = []
        name = item[1]
        contains_num = re.findall("\d", name)
        if not contains_num:
            # print(name)
            for food_item in food_db:
                if Levenshtein.ratio(name, food_item['name_native']) > min_levenshtein_ratio:
                    food_item_matches.append(food_item)
            if food_item_matches:
                match_list.extend(food_item_matches)
            # print(food_item_matches)
    return match_list

def search_algolia(menu_items):
    """
    Use Algolia to search for food items
    :param menu_items:
    :return:
    """
    client = SearchClient.create('Y50RDS26JS', ALGOLIA_SEARCH_API_KEY)
    index = client.init_index(EATS_DB_INDEX)

    food_matches = []
    queries = []
    for item in menu_items:
        name = item[1]
        contains_num = re.findall("\d", name)
        if not contains_num:
            # print(name)
            query_json = {'indexName': 'dev_eats', 'query': name, 'hitsPerPage': 3}
            queries.append(query_json)
    response = client.multiple_queries(queries)
    results = response['results']
    for r in results:
        food_matches.extend(r['hits'])
    return food_matches
