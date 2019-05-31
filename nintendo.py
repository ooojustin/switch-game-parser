import requests
import json
import urllib
import sys

url = "https://u3b6gr4ua3-dsn.algolia.net/1/indexes/*/queries?"
url_params = {
    'x-algolia-agent': 'Algolia for vanilla JavaScript (lite) 3.22.1;JS Helper 2.20.1',
    'x-algolia-application-id': 'U3B6GR4UA3',
    'x-algolia-api-key': '9a20c93440cf63cf1a7008d75f7438bf'
}
url += urllib.parse.urlencode(url_params);

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded'
}

facets = ['generalFilters', 'platform', 'availability', 'categories', 'filterShops', 'virtualConsole', 'characters', 'priceRange', 'esrb', 'filterPlayers']
facets = json.dumps(facets)

def get_games(page):
    "Returns a list of Nintendo Switch games on a specified page number."

    params = {
        'query': '',
        'hitsPerPage': 50,
        'maxValuesPerFacet': 30,
        'page': page,
        'facets': facets,
        'tagFilters': ''
    }

    formData = {
        'requests': [
            {
                'indexName': 'noa_aem_game_en_us',
                'params': urllib.parse.urlencode(params)
            }
        ]
    }

    response = requests.post(url, json.dumps(formData), headers = headers)
    if response.status_code != 200 :
        sys.exit()

    data = json.loads(response.text)
    results = data['results'][0]
    games = results['hits']

    return games
