import re, requests, json

def get_slug(game):
    """Attempts to determine a games slug on metacritic from it's default Nintendo eShop slug."""

    s = '-switch' # if the slug ends with this, remove it
    slug = game['slug']

    if slug.endswith(s):
        slug = slug[:-len(s)]

    return slug
