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
        WHERE (grains.length = ?) 
            AND (grains.spectral_centroid BETWEEN ? AND ?) 
            AND (grains.spectral_flatness BETWEEN ? AND ?) 
            AND (grains.spectral_roll_off_50 BETWEEN ? AND ?) 
            AND (grains.frequency IS NULL) 
            AND (grains.energy > ?) 
            AND (tags.tag = ?)
        GROUP BY grains.id;""",

        # specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) 
            AND (grains.spectral_centroid BETWEEN ? AND ?)
            AND (grains.spectral_flatness BETWEEN ? AND ?) 
            AND (grains.frequency BETWEEN ? AND ?) 
            AND (grains.energy > ?) 
            AND (tags.tag = ?)
        GROUP BY grains.id;""",
    ]

    # Parameter lists
    # The first index is for the select statement index, and the following tuple contains parameters for that select statement
    PARAMS = [
        (1, (length, 100.0, 1000.0, 0.0, 0.3, 100.0, 150.0, 0.05, 'animal')),    # 0
        (0, (length, 100.0, 4000.0, 0.2, 0.6, 800.0, 4500.0, 0.05, 'animal')),   # 1
        (0, (length, 100.0, 4000.0, 0.2, 0.4, 1000.0, 4500.0, 0.05, 'animal')),  # 2
        (1, (length, 100.0, 1000.0, 0.0, 0.5, 100.0, 150.0, 0.05, 'animal')),    # 3
        (1, (length, 100.0, 1000.0, 0.0, 0.3, 100.0, 150.0, 0.05, 'animal')),    # 4
        (0, (length, 100.0, 6000.0, 0.1, 0.8, 100.0, 150.0, 0.05, 'animal')),    # 5
        (0, (length, 100.0, 6000.0, 0.1, 0.2, 1400.0, 4500.0, 0.05, 'animal')),  # 6
        (0, (length, 100.0, 6000.0, 0.0, 0.2, 800.0, 4500.0, 0.05, 'animal')),   # 7
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 200.0, 300.0, 0.05, 'animal')),    # 8
        (1, (length, 100.0, 3000.0, 0.0, 0.3, 200.0, 300.0, 0.05, 'animal')),    # 9
        (1, (length, 100.0, 3000.0, 0.0, 0.4, 200.0, 300.0, 0.05, 'animal')),    # 10
        (1, (length, 100.0, 3000.0, 0.0, 0.5, 200.0, 300.0, 0.05, 'animal')),    # 11
        (0, (length, 100.0, 8000.0, 0.2, 0.4, 100.0, 4500.0, 0.05, 'animal')),   # 12
        (0, (length, 100.0, 8000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'animal')),   # 13
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.05, 'animal')),     # 14
        (0, (length, 100.0, 7000.0, 0.2, 0.4, 100.0, 4500.0, 0.05, 'animal')),   # 15
        (0, (length, 100.0, 6000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'animal')),   # 16
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.05, 'animal')),     # 17
        (1, (length, 100.0, 2000.0, 0.0, 0.4, 100.0, 4500.0, 0.05, 'animal')),   # 18
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'animal')),   # 19
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 500.0, 650.0, 0.05, 'animal')),    # 20
        (1, (length, 100.0, 5000.0, 0.0, 0.4, 700.0, 2000.0, 0.01, 'animal')),   # 21
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'animal')),   # 22
        (1, (length, 100.0, 5000.0, 0.0, 0.2, 700.0, 2050.0, 0.01, 'animal')),   # 23
        (0, (length, 100.0, 3000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'animal')),   # 24
    ]

    
    # Retrieve grain metadata and grains
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


def query3(length, cursor) -> list:
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
        WHERE (grains.length = ?) 
            AND (grains.spectral_centroid BETWEEN ? AND ?) 
            AND (grains.spectral_flatness BETWEEN ? AND ?) 
            AND (grains.spectral_roll_off_50 BETWEEN ? AND ?) 
            AND (grains.frequency IS NULL) 
            AND (grains.energy > ?) 
            AND (tags.tag = ? OR tags.tag = ?)
        GROUP BY grains.id;""",

        # specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) 
            AND (grains.spectral_centroid BETWEEN ? AND ?)
            AND (grains.spectral_flatness BETWEEN ? AND ?) 
            AND (grains.frequency BETWEEN ? AND ?) 
            AND (grains.energy > ?) 
            AND (tags.tag = ? OR tags.tag = ?)
        GROUP BY grains.id;""",
    ]

    # Parameter lists
    # The first index is for the select statement index, and the following tuple contains parameters for that select statement
    PARAMS = [
        (1, (length, 50.0, 10000.0, 0.0, 0.3, 420.0, 460.0, 0.01, 'bell', 'metal')),    # 0
        (0, (length, 100.0, 4000.0, 0.2, 0.6, 800.0, 4500.0, 0.01, 'bell', 'metal')),   # 1
        (0, (length, 100.0, 4000.0, 0.2, 0.4, 1000.0, 4500.0, 0.01, 'city', 'engine')),  # 2
        (1, (length, 50.0, 10000.0, 0.0, 0.5, 420.0, 460.0, 0.01, 'bell', 'engine')),    # 3
        (1, (length, 50.0, 10000.0, 0.0, 0.3, 420.0, 460.0, 0.01, 'city', 'engine')),    # 4
        (0, (length, 100.0, 6000.0, 0.1, 0.8, 100.0, 150.0, 0.01, 'city', 'metal')),  # 5
        (0, (length, 100.0, 6000.0, 0.1, 0.2, 1400.0, 4500.0, 0.01, 'city', 'engine')),  # 6
        (0, (length, 100.0, 6000.0, 0.0, 0.2, 800.0, 4500.0, 0.01, 'city', 'metal')),   # 7
        (1, (length, 100.0, 3000.0, 0.0, 0.8, 800.0, 900.0, 0.01, 'bell', 'metal')),   # 8
        (1, (length, 100.0, 3000.0, 0.0, 0.8, 800.0, 900.0, 0.01, 'bell', 'metal')),    # 9
        (1, (length, 100.0, 3000.0, 0.0, 0.8, 800.0, 1200.0, 0.01, 'city', 'engine')),   # 10
        (1, (length, 100.0, 3000.0, 0.0, 0.8, 800.0, 1200.0, 0.01, 'city', 'engine')),    # 11
        (0, (length, 100.0, 8000.0, 0.5, 0.9, 100.0, 4500.0, 0.01, 'city', 'engine')),   # 12
        (0, (length, 100.0, 8000.0, 0.4, 0.9, 100.0, 4500.0, 0.01, 'city', 'instrument')),   # 13
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.01, 'city', 'engine')),     # 14
        (0, (length, 100.0, 7000.0, 0.3, 0.9, 100.0, 4500.0, 0.01, 'city', 'instrument')),   # 15
        (0, (length, 100.0, 6000.0, 0.0, 0.05, 100.0, 4500.0, 0.01, 'city', 'engine')),   # 16
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.01, 'instrument', 'metal')),     # 17
        (1, (length, 100.0, 2000.0, 0.0, 0.4, 100.0, 4500.0, 0.01, 'city', 'engine')),   # 18
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 100.0, 4500.0, 0.01, 'city', 'engine')),   # 19
        (0, (length, 100.0, 1000.0, 0.0, 0.9, 500.0, 650.0, 0.01, 'city', 'engine')),    # 20
        (1, (length, 100.0, 5000.0, 0.0, 0.4, 700.0, 2000.0, 0.01, 'instrument', 'engine')),   # 21
        (0, (length, 100.0, 1000.0, 0.0, 0.9, 100.0, 4500.0, 0.01, 'city', 'engine')),   # 22
        (1, (length, 100.0, 5000.0, 0.0, 0.2, 700.0, 2050.0, 0.01, 'bell', 'engine')),   # 23
        (0, (length, 100.0, 3000.0, 0.0, 0.9, 100.0, 4500.0, 0.01, 'city', 'engine')),   # 24
    ]

    
    # Retrieve grain metadata and grains
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


def query4(length, cursor) -> list:
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
        WHERE (grains.length = ?) 
            AND (grains.spectral_centroid BETWEEN ? AND ?) 
            AND (grains.spectral_flatness BETWEEN ? AND ?) 
            AND (grains.spectral_roll_off_50 BETWEEN ? AND ?) 
            AND (grains.frequency IS NULL) 
            AND (grains.energy > ?) 
            AND (tags.tag = ?)
        GROUP BY grains.id;""",

        # specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) 
            AND (grains.spectral_centroid BETWEEN ? AND ?)
            AND (grains.spectral_flatness BETWEEN ? AND ?) 
            AND (grains.frequency BETWEEN ? AND ?) 
            AND (grains.energy > ?) 
            AND (tags.tag = ?)
        GROUP BY grains.id;""",
    ]

    # Parameter lists
    # The first index is for the select statement index, and the following tuple contains parameters for that select statement
    PARAMS = [
        (0, (length, 100.0, 3000.0, 0.1, 0.9, 50.0, 1000.0, 0.05, 'obama')),    # 0
        (0, (length, 100.0, 4000.0, 0.1, 0.9, 40.0, 1000.0, 0.05, 'obama')),   # 1
        (1, (length, 100.0, 4000.0, 0.1, 0.4, 30.0, 130.0, 0.05, 'obama')),  # 2
        (0, (length, 100.0, 3000.0, 0.0, 0.5, 20.0, 1200.0, 0.05, 'obama')),    # 3
        (0, (length, 100.0, 1000.0, 0.0, 0.3, 50.0, 1500.0, 0.05, 'obama')),    # 4
        (0, (length, 100.0, 6000.0, 0.1, 0.8, 100.0, 1550.0, 0.05, 'obama')),  # 5
        (0, (length, 100.0, 6000.0, 0.1, 0.2, 1400.0, 4500.0, 0.05, 'obama')),  # 6
        (1, (length, 100.0, 6000.0, 0.0, 0.2, 400.0, 900.0, 0.05, 'obama')),   # 7
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 600.0, 1200.0, 0.05, 'obama')),   # 8
        (0, (length, 100.0, 3000.0, 0.1, 0.3, 200.0, 300.0, 0.05, 'obama')),    # 9
        (1, (length, 100.0, 3000.0, 0.0, 0.4, 800.0, 1200.0, 0.05, 'obama')),   # 10
        (1, (length, 100.0, 3000.0, 0.0, 0.5, 600.0, 1200.0, 0.05, 'obama')),    # 11
        (0, (length, 10.0, 8000.0, 0.15, 0.9, 100.0, 10000.0, 0.05, 'obama')),   # 12
        (0, (length, 10.0, 8000.0, 0.1, 0.2, 100.0, 4500.0, 0.05, 'obama')),   # 13
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.05, 'obama')),     # 14
        (0, (length, 10.0, 7000.0, 0.1, 0.4, 100.0, 4500.0, 0.05, 'obama')),   # 15
        (0, (length, 10.0, 6000.0, 0.1, 0.4, 100.0, 4500.0, 0.05, 'obama')),   # 16
        (1, (length, 100.0, 3000.0, 0.0, 0.1, 20.0, 120.0, 0.05, 'obama')),     # 17
        (1, (length, 100.0, 2000.0, 0.0, 0.4, 500.0, 4500.0, 0.05, 'obama')),   # 18
        (0, (length, 100.0, 5000.0, 0.1, 0.5, 100.0, 4500.0, 0.05, 'obama')),   # 19
        (0, (length, 100.0, 5000.0, 0.1, 0.6, 500.0, 650.0, 0.05, 'obama')),    # 20
        (1, (length, 100.0, 5000.0, 0.0, 0.4, 700.0, 2000.0, 0.01, 'obama')),   # 21
        (0, (length, 100.0, 5000.0, 0.1, 0.9, 100.0, 4500.0, 0.05, 'obama')),   # 22
        (1, (length, 100.0, 5000.0, 0.0, 0.2, 800.0, 2050.0, 0.01, 'obama')),   # 23
        (0, (length, 100.0, 8000.0, 0.15, 0.9, 100.0, 1500.0, 0.05, 'obama')),   # 24
        (0, (length, 100.0, 8000.0, 0.15, 0.9, 100.0, 2500.0, 0.05, 'obama')),   # 25
        (0, (length, 100.0, 9000.0, 0.15, 0.9, 100.0, 3500.0, 0.05, 'obama')),   # 26
        (0, (length, 100.0, 10000.0, 0.15, 0.9, 100.0, 4500.0, 0.05, 'obama')),   # 27
        (1, (length, 100.0, 8000.0, 0.0, 0.1, 100.0, 5500.0, 0.05, 'obama')),   # 28
        (1, (length, 100.0, 5000.0, 0.0, 0.1, 50.0, 150.0, 0.05, 'obama')),   # 29
    ]

    
    # Retrieve grain metadata and grains
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
