import mysql.connector, json, os

# initialize the database connection
if os.path.isfile('database.cfg'):

    db_cfg = json.loads(open('database.cfg', 'r').read())
    db = mysql.connector.connect(
        host = db_cfg['host'],
        user = db_cfg['username'],
        password = db_cfg['password']
    )

    db.autocommit = True # automatically commit changes to db (ex: insert queries)
    cursor = db.cursor() # object used to execute commands

def get_game(id):
    """
    Gets a games existing data from our database.

    Parameters:
        id (string): The id of the game in the database.

    Returns:
        tuple: A tuple representing the row of the game in the database.
    """
    cursor.execute("SELECT * FROM games WHERE id LIKE '{}'".format(id))
    return cursor.fetchone()

def delete_game(id):
    """
    Deletes a game from our database.

    Parameters:
        id (string): The id of the game in the database.
    """
    cursor.execute("DELETE FROM games WHERE id='{}'".format(id))

def insert_game(game):
    """
    Uploads information about a game to our database.

    Parameters:
        game (dict): A dict containing the games information, deserialized from algolia response.
    """

    # make sure the game actually has an id.
    if not 'id' in game:
        return

    # skip the game, if it's already uploaded (and the data is up-to-date...)
    # note: 14 = index of 'modified' column
    row = get_game(game['id'])
    if row:
        if game['lastModified'] > row[14]:
            delete_game(game['id'])
        else: return

    # fix some values that might not exist
    patchers = ('msrp', 'salePrice', 'gallery')
    for patcher in patchers:
        if not patcher in game:
            game[patcher] = None

    # handle json arrays (serialize them into strings, store as text)
    json_vars = ('characters', 'categories', 'publishers', 'developers', 'availability')
    for var in json_vars:
        if var in game:
            game[var] = json.dumps(game[var])
        else:
            game[var] = "[]"

    # values to upload via insert query
    params = []
    param_names = (
        'id', 'slug', 'locale',
        'title', 'description', 'msrp',
        'salePrice', 'boxArt', 'gallery',
        'characters', 'categories', 'publishers',
        'developers', 'availability', 'lastModified')
    for param_name in param_names:
        params.append(game[param_name])

    # insert game data into 'games' table
    cursor.execute("""INSERT INTO games (
        id, slug, locale,
        title, description, price,
        sale_price, art, gallery,
        characters, categories, publishers,
        developers, availability, modified) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )""", params)

def init():
    """
    Creates the database/all needed tables used in the program.
    If the database already exists, nothing will be executed.
    """

    # if the database already exists, return
    cursor.execute("SHOW DATABASES LIKE 'switch_game_parser'")
    if cursor.fetchone():
        cursor.execute("USE switch_game_parser")
        return

    # create database on mysql server
    cursor.execute("CREATE DATABASE switch_game_parser")

    # use the database (we'll create tables in here)
    cursor.execute("USE switch_game_parser")

    # create 'games' table
    cursor.execute("""
        CREATE TABLE `games` (
        	`id` VARCHAR(32) NOT NULL,
        	`slug` TEXT NOT NULL,
        	`locale` TEXT NOT NULL,
        	`title` TEXT NOT NULL,
        	`description` TEXT NOT NULL,
        	`price` FLOAT NULL DEFAULT NULL,
        	`sale_price` FLOAT NULL DEFAULT NULL,
        	`art` TEXT NOT NULL,
        	`gallery` TEXT NULL,
        	`characters` TEXT NOT NULL,
        	`categories` TEXT NOT NULL,
        	`publishers` TEXT NOT NULL,
        	`developers` TEXT NOT NULL,
        	`availability` TEXT NOT NULL,
            `modified` BIGINT(20) NOT NULL,
        	PRIMARY KEY (`id`)
        )
        COLLATE = 'utf8mb4_general_ci'
        ENGINE = InnoDB;
    """)
