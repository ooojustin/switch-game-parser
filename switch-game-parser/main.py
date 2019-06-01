import json, nintendo, metacritic, database

if __name__ == "__main__":

    # database initialization
    database.init()

    page = 0
    count = 0

    while True:

        games = nintendo.get_games(page)

        if len(games) == 0:
            break;

        for game in games:
            count += 1;
            # rating = metacritic.get_metacritic_score(game)
            print(str(count) + ": " + game['title'])
            database.insert_game(game)
            
        page += 1
