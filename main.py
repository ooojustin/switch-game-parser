import nintendo

page = 0
count = 0

while True:

    games = nintendo.get_games(page)

    if len(games) == 0:
        break;

    for game in games:
        count += 1;
        print(str(count) + ": " + game['title'])

    page += 1

# template:
# https://www.metacritic.com/search/game/moonlighter/results?plats[268409]=1&search_type=advanced
