import psycopg

class CommanderDBClient:
    def __init__(self, db_url: str):
        self.conn = psycopg.connect(db_url)
        
    def create_player_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            self.conn.commit()
            
    def create_commander_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS commanders (
                    commander_id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    color TEXT,
                    color_identity TEXT NOT NULL,
                    mana_value INT,
                    mana_cost TEXT,
                    card_type TEXT,
                    subtype TEXT,
                    card_text TEXT
                )
            """)
            self.conn.commit()
            
    def create_deck_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS decks (
                    deck_id SERIAL PRIMARY KEY,
                    player_id INT REFERENCES players(player_id)
                )
            """)
            self.conn.commit()
            
    def create_deck_commanders_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS deck_commanders (
                    deck_id INT REFERENCES decks(deck_id),
                    commander_id INT REFERENCES commanders(commander_id),
                    PRIMARY KEY (deck_id, commander_id)
                )
            """)
            self.conn.commit()
            
    def create_game_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    game_id SERIAL PRIMARY KEY,
                    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    num_players INT NOT NULL,
                    variant TEXT NOT NULL
                )
            """)
            self.conn.commit()
            
    def create_game_players_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_players (
                    game_id INT REFERENCES games(game_id),
                    player_id INT REFERENCES players(player_id),
                    deck_id INT REFERENCES decks(deck_id),
                    PRIMARY KEY (game_id, player_id)
                )
            """)
            self.conn.commit()
