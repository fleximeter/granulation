"""
File: query.py

This file contains query methods.
"""

import grain.grain_sql as grain_sql

def query1(length, cursor) -> list:
    """
    Queries the database and returns a list of grain data lists
    :param length: The target grain length
    :return: A list of grain data lists
    """
    
    # The select statements to use
    SELECT = [
        # not specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) AND (grains.spectral_flatness BETWEEN ? AND ?) AND (grains.spectral_roll_off_75 BETWEEN ? AND ?) 
            AND (grains.energy > ?) AND (grains.frequency IS NULL) AND (tags.tag = ?)
        GROUP BY grains.id;""",

        # specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) AND (grains.spectral_flatness BETWEEN ? AND ?) AND (grains.spectral_roll_off_75 BETWEEN ? AND ?) 
            AND (grains.energy > ?) AND (grains.frequency BETWEEN ? AND ?) AND (tags.tag = ?)
        GROUP BY grains.id;""",
    ]

    # Parameter lists
    # The first index is for the select statement index, and the following tuple contains parameters for that select statement
    PARAMS = [
        (0, (length, 0.4, 1.0, 200.0, 400.0, 0.05, 'animal')),
        (0, (length, 0.3, 0.6, 250.0, 450.0, 0.05, 'animal')),
        (0, (length, 0.3, 0.6, 300.0, 500.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.5, 350.0, 550.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.3, 400.0, 600.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.3, 450.0, 650.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.2, 500.0, 700.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 550.0, 750.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 600.0, 750.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.3, 650.0, 800.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.3, 700.0, 850.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.4, 650.0, 800.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.4, 600.0, 750.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 550.0, 700.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 500.0, 650.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 500.0, 600.0, 0.05, 'animal')),
    ]

    
    # Retrieve grain metadata and grains
    print("Retrieving grains...")
    grain_entry_categories = []
    for i, param in enumerate(PARAMS):
        cursor.execute(SELECT[param[0]], param[1])
        records = cursor.fetchall()
        if len(records) == 0:
            raise Exception(f"No grains found for index {i}.")
        entry_category = []
        for record in records:
            entry_category.append({grain_sql.FIELDS[i]: record[i] for i in range(len(record))})
        grain_entry_categories.append(entry_category)

    return grain_entry_categories



def query2(length, cursor) -> list:
    """
    Queries the database and returns a list of grain data lists
    :param length: The target grain length
    :return: A list of grain data lists
    """
    
    # The select statements to use
    SELECT = [
        # not specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) AND (grains.spectral_flatness BETWEEN ? AND ?) AND (grains.spectral_roll_off_75 BETWEEN ? AND ?) 
            AND (grains.energy > ?) AND (grains.frequency IS NULL) AND (tags.tag = ?)
        GROUP BY grains.id;""",

        # specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) AND (grains.spectral_flatness BETWEEN ? AND ?) AND (grains.spectral_roll_off_75 BETWEEN ? AND ?) 
            AND (grains.energy > ?) AND (grains.frequency BETWEEN ? AND ?) AND (tags.tag = ?)
        GROUP BY grains.id;""",
    ]

    # Parameter lists
    # The first index is for the select statement index, and the following tuple contains parameters for that select statement
    PARAMS = [
        (0, (length, 0.4, 1.0, 200.0, 400.0, 0.05, 'animal')),
        (0, (length, 0.3, 0.6, 250.0, 450.0, 0.05, 'animal')),
        (0, (length, 0.3, 0.6, 300.0, 500.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.5, 350.0, 550.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.3, 400.0, 600.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.3, 450.0, 650.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.2, 500.0, 700.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 550.0, 750.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 600.0, 750.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.3, 650.0, 800.0, 0.05, 'animal')),
        (0, (length, 0.1, 0.3, 700.0, 850.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.4, 650.0, 800.0, 0.05, 'animal')),
        (0, (length, 0.2, 0.4, 600.0, 750.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 550.0, 700.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 500.0, 650.0, 0.05, 'animal')),
        (0, (length, 0.0, 0.2, 500.0, 600.0, 0.05, 'animal')),
    ]

    
    # Retrieve grain metadata and grains
    print("Retrieving grains...")
    grain_entry_categories = []
    for i, param in enumerate(PARAMS):
        cursor.execute(SELECT[param[0]], param[1])
        records = cursor.fetchall()
        if len(records) == 0:
            raise Exception(f"No grains found for index {i}.")
        entry_category = []
        for record in records:
            entry_category.append({grain_sql.FIELDS[i]: record[i] for i in range(len(record))})
        grain_entry_categories.append(entry_category)

    return grain_entry_categories
