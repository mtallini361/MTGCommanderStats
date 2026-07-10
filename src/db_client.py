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
