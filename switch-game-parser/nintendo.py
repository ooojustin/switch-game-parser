import requests, json, urllib

URL_PARAMS = {
    'x-algolia-agent': 'Algolia for vanilla JavaScript (lite) 3.22.1;JS Helper 2.20.1',
    'x-algolia-application-id': 'U3B6GR4UA3',
    'x-algolia-api-key': '9a20c93440cf63cf1a7008d75f7438bf'
}
URL = "https://u3b6gr4ua3-dsn.algolia.net/1/indexes/*/queries?" + urllib.parse.urlencode(URL_PARAMS);

HEADERS = {
    'user-agent': 'switch-game-parser',
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded'
}

FACETS = json.dumps([
    'generalFilters', 'platform', 'availability',
    'categories', 'filterShops', 'virtualConsole',
    'characters', 'priceRange',
    'esrb', 'filterPlayers'])

def get_games(page):
    """
    Gets a list of Nintendo Switch games on a specified page number.
    The list contains objects deserialized from the following json format: https://pastebin.com/2VKV9vpk

    Parameters:
        page (int): The page number to search for games on.

    Returns:
        list: A list of game dicts.
    """

    params = {
        'query': '',
        'hitsPerPage': 50,
        'maxValuesPerFacet': 30,
        'page': page,
        'facets': FACETS,
        'tagFilters': '',
        'facetFilters': ("platform:Nintendo Switch")
    }

    formData = {
        'requests': [
            {
                'indexName': 'noa_aem_game_en_us',
                'params': urllib.parse.urlencode(params)
            }
        ]
    }

    response = requests.post(URL, json.dumps(formData), headers = HEADERS)
    if response.status_code != 200 :
        sys.exit()

    data = json.loads(response.text)
    results = data['results'][0]
    games = results['hits']

    return games
