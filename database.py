import mysql.connector, json

# initialize the database connection
db_cfg = json.loads(open('database.cfg', 'r').read())
db = mysql.connector.connect(
    host = db_cfg['host'],
    user = db_cfg['username'],
    password = db_cfg['password']
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
          `id` varchar(32) NOT NULL,
          `slug` text NOT NULL,
          `locale` text NOT NULL,
          `title` text NOT NULL,
          `description` text NOT NULL,
          `art` text NOT NULL,
          `gallery` varchar(32) NOT NULL,
          `characters` text NOT NULL,
          `categories` text NOT NULL,
          `publishers` text NOT NULL,
          `developers` text NOT NULL,
          `availability` text NOT NULL,
          `modified` bigint(20) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # set the 'id' column to the primary
    cursor.execute("ALTER TABLE `games` ADD PRIMARY KEY (`id`);")
