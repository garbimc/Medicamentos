import sqlite3

# Function to create the database and the table
def criar_tabela():
    conn = sqlite3.connect("medicamentos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            concentracao_mg REAL,
            concentracao_ml REAL,
            dose_minima_kg_dia REAL,
            dose_maxima_kg_dia REAL,
            volume_embalagem_ml REAL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
criar_tabela()
