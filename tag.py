"""
File: tag.py

This is a grain tagger.
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
               SELECT id FROM grains WHERE
               (file LIKE '%metal%')
               """)
items = cursor.fetchall()
cursor.executemany("""
                   INSERT INTO tags (grain_id, tag)
                   VALUES (?, 'metal');
                   """, items)

db.commit()
