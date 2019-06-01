import re, requests, json

# format of a game url on metacritic website
GAME_URL = 'https://www.metacritic.com/game/switch/{}'

# regular expression to find json data about game in metacritic page
JSON_EXPRESSION = r'<script type=\"application/ld\+json\">.*?</script>'

# headers to use for metacritic request. user-agent must be defined to prevent 403.
HEADERS = {
    'user-agent': 'switch-game-parser'
}

def get_slug(game):
    """Attempts to determine a games slug on metacritic from it's default Nintendo eShop slug."""

    s = '-switch' # if the slug ends with this, remove it
    slug = game['slug']

    if slug.endswith(s):
        slug = slug[:-len(s)]

    return slug

def get_metacritic_score(game):
    """Attempts to retreieve a games metacritic rating. Returns 'False' if failed, for any reason."""

    # determine metacritic page url
    slug = get_slug(game)
    url = GAME_URL.format(slug)

    # download metacritic page
    response = requests.get(url, headers = HEADERS)
    if response.status_code != 200:
        return False

    # use regular expressions to match metacritic json data from html response
    match = re.search(JSON_EXPRESSION, response.text, re.MULTILINE | re.DOTALL)

    if not match:
        return False

    # the raw match, with 'script' tags
    data = match.group()

    # remove script tags by removing first & last line of match
    data = data.split("\n", 1)[1] # remove first line
    data = data[:data.rfind('\n')] # remove last line

    # load raw data into object
    data = json.loads(data)

    # make sure we have a rating
    if not 'aggregateRating' in data:
        return False

    # return the metacritic score
    return data['aggregateRating']['ratingValue']
