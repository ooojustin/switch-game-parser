import mysql.connector, json

# initialize the database connection
db_cfg = json.loads(open('database.cfg', 'r').read())
db = mysql.connector.connect(
    host = db_cfg['host'],
    user = db_cfg['username'],
    password = db_cfg['password']
)

def insert_game(game):

    # values to upload via insert query
    params = (
        game['id'],                         # id
        game['slug'],                       # slug
        game['locale'],                     # locale
        game['title'],                      # title
        game['description'],                # description
        game['msrp'],                       # price
        game['salePrice'],                  # sale price
        game['boxArt'],                     # art
        game['gallery'],                    # gallery
        json.dumps(game['characters']),     # characters
        json.dumps(game['categories']),     # categories
        json.dumps(game['publishers']),     # publishers
        json.dumps(game['developers']),     # developers
        json.dumps(game['availability']),   #availability
        game['lastModified']                # modified
        )



# database init function, only runs once ever
def init():
    """
    Creates the database/all needed tables used in the program.
    If the database already exists, nothing will be executed.
    """

    # if the database already exists, return
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES LIKE 'switch_game_parser'")
    if cursor.fetchone():
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
        	`gallery` VARCHAR(32) NOT NULL,
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
