get_db()

import sqlite3

# SQLite DB (auto-created)
conn = sqlite3.connect("sme_ai.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS business_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sales REAL,
    expenses REAL,
    profit REAL,
    health_score INTEGER,
    risk_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()