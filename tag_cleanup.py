"""
File: tag_cleanup.py

This script cleans up duplicate grain tags.
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

cursor.execute("DELETE FROM tags WHERE rowid NOT IN (SELECT MIN(rowid) FROM tags GROUP BY grain_id, tag);")

db.commit()
db.close()
