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

# If a file path contains the following keyword, the associated list of tags applies to that grain.
tags = {
    "bird": ["bird", "animal"],
    "raven": ["raven", "bird", "animal"],
    "goose": ["goose", "bird", "animal"],
    "geese": ["goose", "bird", "animal"],
    "duck": ["duck", "bird", "animal"],
    "frog": ["frog", "animal"],
    "toad": ["toad", "animal"],
    "night-sounds": ["animal"],
    "cat": ["cat", "animal"],
    "purring": ["purring", "cat", "animal"],
    "lion": ["lion", "animal"],
    "cow": ["cow", "animal", "farm"],
    "cricket": ["cricket", "bug", "animal"],
    "barn": ["barn", "farm"],
    "kansas-night": ["animal"],
    "yukon": ["yukon", "place"],
    "france": ["france", "place"],
    "brasil": ["brazil", "place"],
    "chime": ["chime", "bell", "instrument"],
    "bell": ["bell", "instrument"],
    "glass": ["glass", "instrument"],
    "gong": ["gong", "bell", "instrument"],
    "violin": ["violin", "instrument"],
    "flute": ["flute", "instrument"],
    "metal": ["metal", "instrument"],
    "city": ["city"],
    "train": ["city", "train"],
    "street": ["city"],
    "friction": ["friction"],
    "truck": ["truck", "engine"],
    "snowmobile": ["snowmobile", "engine"],
    "foley": ["foley"],
    "noaa-weather": ["weather", "voice", "noaa"],
    "speech": ["speech", "voice"],
    "jfk": ["jfk"],
    "nixon": ["nixon"],
    "watergate": ["watergate"],
    "obama": ["obama"],
    "fdr": ["fdr"],
}

print("Tagging...")
for key, val in tags.items():
    cursor.execute("SELECT id FROM grains WHERE LOWER(file) LIKE ?;", (f"%{key}%",))
    items = cursor.fetchall()
    for tag in val:
        for grain in items:
            cursor.execute("INSERT INTO tags (grain_id, tag) VALUES (?, ?);", (grain[0], tag))
db.commit()

# clean up duplicate tags
print("Cleaning up duplicate tags...")
cursor.execute("DELETE FROM tags WHERE rowid NOT IN (SELECT MIN(rowid) FROM tags GROUP BY grain_id, tag);")
db.commit()

db.close()
print("Done.")
