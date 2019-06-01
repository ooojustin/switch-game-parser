import time, json, nintendo, metacritic, database

# minutes betwen loop calls
LOOP_INTERVAL = 10

def loop_games():
    """Loops through Nintendo Switch games and handles them."""

    page = 0
    count = 0

    # breaks when there are no more games left
    while True:

        games = nintendo.get_games(page)

        if len(games) == 0:
            break;

        for game in games:
            count += 1;
            print(str(count) + ": " + game['title'])
            database.insert_game(game)

        page += 1

if __name__ == "__main__":

    # database initialization
    database.init()

    while True:

        # run game loop
        loop_games()

        # delay before running loop again
        print("executing again in " + str(LOOP_INTERVAL) + " minute(s)...")
        time.sleep(LOOP_INTERVAL * 60)
