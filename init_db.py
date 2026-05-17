import sqlite3

conn = sqlite3.connect('garden.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        sunlight INTEGER,
        temperature REAL,
        humidity REAL,
        system_mode TEXT
    )
''')
conn.commit()
conn.close()
print("Database 'garden.db' created successfully!")