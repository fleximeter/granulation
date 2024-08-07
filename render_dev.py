"""
File: render_dev.py

This grain realizer is for experimentation.
"""

import grain.grain_sql as grain_sql
import aus.audiofile as audiofile
import aus.operations as operations
import random
import scipy.signal as signal
from grain.effects import *
import grain.grain_assembler as grain_assembler


if __name__ == "__main__":
    rng = random.Random()
    rng.seed()
    
    effect_chain = [
        ButterworthFilterEffect(50, "highpass", 4)
    ]
    effect_cycle = [
        IdentityEffect(), 
        IdentityEffect(), 
        ChorusEffect(2, 0.5, 20, 0.4, 0.5),
        ButterworthFilterEffect(440, "lowpass", 2),
        IdentityEffect(), 
        IdentityEffect(), 
        ButterworthFilterEffect(440, "lowpass", 2),
        ChorusEffect(2, 0.5, 20, 0.4, 0.5),
    ]

    # The directory containing the files that were analyzed. We can search in here for the files,
    # even if the path doesn't match exactly. This is needed because we may have performed
    # the analysis on a different computer.
    SOURCE_DIR = "D:\\Recording\\Samples\\freesound\\creative_commons_0\\granulation"
    
    # The database
    DB_FILE = "D:\\Recording\\data\\grains.sqlite3"

    SELECT = """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) AND (grains.spectral_flatness BETWEEN ? AND ?) AND (grains.spectral_roll_off_75 BETWEEN ? AND ?) 
            AND (grains.energy > ?) AND (grains.frequency IS NULL) AND (tags.tag = ?)
        GROUP BY grains.id;"""

    db, cursor = grain_sql.connect_to_db(DB_FILE)
    entries = cursor.execute(SELECT, (4096, 0.0, 0.2, 200.0, 500.0, 0.05, 'animal'))
    vals = cursor.fetchall()
    print(vals)
