# src/banco.py
import sqlite3

def criar_bd(path='data/bd.sqlite'):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            data TEXT,
            risco REAL
        )
    ''')

    conn.commit()
    conn.close()
