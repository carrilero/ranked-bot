# utils.py

import os
import random
import psycopg2
from psycopg2.extras import RealDictCursor

def pick_random_host(players):
    """
    Elige aleatoriamente un host de la lista de jugadores.
    """
    if not players:
        raise ValueError("La lista de jugadores está vacía.")
    return random.choice(players)

def get_db_connection():
    """
    Devuelve una conexión a la base de datos PostgreSQL usando DATABASE_URL
    configurada en las variables de entorno.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("No se encontró la variable de entorno DATABASE_URL")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    """
    Crea las tablas 'users' y 'match_history' si no existen.
    Debe llamarse una vez al arrancar el bot para asegurar que el esquema existe.
    """
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
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(schema)
        conn.commit()
        print("✅ Tablas de la base de datos inicializadas.")
    except Exception as e:
        print(f"❌ Error inicializando la base de datos: {e}")
    finally:
        if conn:
            conn.close()
