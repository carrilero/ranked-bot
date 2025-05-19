from utils import get_db_connection

schema = """
CREATE TABLE IF NOT EXISTS users (
    discord_id BIGINT PRIMARY KEY,
    username TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS match_history (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    team1 TEXT[],
    team2 TEXT[],
    winner TEXT
);
"""

if __name__ == "__main__":
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(schema)
        conn.commit()
        cur.close()
        conn.close()
        print("Tablas creadas correctamente.")
    except Exception as e:
        print("Error creando las tablas:", e)
