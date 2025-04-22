import sqlite3

def datu_bazes_izveide():
    conn = sqlite3.connect('lietotajs.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lietotajs (
            id INTEGER PRIMARY KEY,
            vards TEXT,
            uzvards TEXT)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meklejumi (
            id INTEGER PRIMARY KEY,
            lietotaja_id INTEGER,
            nosaukums TEXT,
            autors TEXT,
            FOREIGN KEY (lietotaja_id) REFERENCES users (id))
    """)
    conn.commit()
    conn.close()