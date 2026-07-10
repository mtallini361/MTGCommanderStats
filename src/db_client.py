import psycopg

class CommanderDBClient:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def get_commander_by_name(self, name: str) -> dict:
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM commanders WHERE name = %s", (name,))
                row = cur.fetchone()
                if row is None:
                    raise ValueError(f"Commander '{name}' not found in database")
                return dict(row)