import sqlite3

conn = sqlite3.connect("voting_system.db")
cursor = conn.cursor()

# Voters table
cursor.execute("""
CREATE TABLE IF NOT EXISTS voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    face_encoding BLOB,
    image_path TEXT,
    has_voted INTEGER DEFAULT 0
)
""")

# Candidates table
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    votes INTEGER DEFAULT 0
)
""")

# Insert candidates
cursor.executemany("""
INSERT OR IGNORE INTO candidates (name)
VALUES (?)
""", [
    ("Candidate A",),
    ("Candidate B",),
    ("Candidate C",)
])

conn.commit()
conn.close()

print("✅ Database ready")
