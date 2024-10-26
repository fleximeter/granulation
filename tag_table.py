"""
File: tag_table.py

Makes the tag table
"""

import os
import platform
import sqlite3

MAC = "/Users/jmartin50/recording"
ARGON = "/Users/jmartin50/recording"
PC = "D:\\recording"
SYSTEM = platform.system()

if SYSTEM == "Darwin":
    DB = os.path.join(MAC, "data/grains.sqlite3")
elif SYSTEM == "Linux":
    DB = os.path.join(ARGON, "data/grains.sqlite3")
else:
    DB = os.path.join(PC, "data/grains.sqlite3")

db = sqlite3.connect(DB)
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE tags (
        id INTEGER PRIMARY KEY,
        grain_id INTEGER NOT NULL,
        tag TEXT NOT NULL,
        FOREIGN KEY (grain_id) REFERENCES grains(id)
    );
""")

db.commit()
db.close()
