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
            AND (tags.tag = ?)
        GROUP BY grains.id;""",
    ]

    # Parameter lists
    # The first index is for the select statement index, and the following tuple contains parameters for that select statement
    PARAMS = [
        (1, (length, 100.0, 1000.0, 0.0, 0.3, 100.0, 150.0, 0.05, 'city', 'engine')),    # 0
        (0, (length, 100.0, 4000.0, 0.2, 0.6, 800.0, 4500.0, 0.05, 'city', 'engine')),   # 1
        (0, (length, 100.0, 4000.0, 0.2, 0.4, 1000.0, 4500.0, 0.05, 'city', 'engine')),  # 2
        (1, (length, 100.0, 1000.0, 0.0, 0.5, 100.0, 150.0, 0.05, 'city', 'engine')),    # 3
        (1, (length, 100.0, 1000.0, 0.0, 0.3, 100.0, 150.0, 0.05, 'city', 'engine')),    # 4
        (0, (length, 100.0, 6000.0, 0.1, 0.8, 100.0, 150.0, 0.05, 'city', 'engine')),  # 5
        (0, (length, 100.0, 6000.0, 0.1, 0.2, 1400.0, 4500.0, 0.05, 'city', 'engine')),  # 6
        (0, (length, 100.0, 6000.0, 0.0, 0.2, 800.0, 4500.0, 0.05, 'city', 'engine')),   # 7
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 200.0, 300.0, 0.05, 'city', 'engine')),   # 8
        (1, (length, 100.0, 3000.0, 0.0, 0.3, 200.0, 300.0, 0.05, 'city', 'engine')),    # 9
        (1, (length, 100.0, 3000.0, 0.0, 0.4, 200.0, 300.0, 0.05, 'city', 'engine')),   # 10
        (1, (length, 100.0, 3000.0, 0.0, 0.5, 200.0, 300.0, 0.05, 'city', 'engine')),    # 11
        (0, (length, 100.0, 8000.0, 0.2, 0.4, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 12
        (0, (length, 100.0, 8000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 13
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.05, 'city', 'engine')),     # 14
        (0, (length, 100.0, 7000.0, 0.2, 0.4, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 15
        (0, (length, 100.0, 6000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 16
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.05, 'city', 'engine')),     # 17
        (1, (length, 100.0, 2000.0, 0.0, 0.4, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 18
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 19
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 500.0, 650.0, 0.05, 'city', 'engine')),    # 20
        (1, (length, 100.0, 5000.0, 0.0, 0.4, 700.0, 2000.0, 0.01, 'city', 'engine')),   # 21
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 22
        (1, (length, 100.0, 5000.0, 0.0, 0.2, 700.0, 2050.0, 0.01, 'city', 'engine')),   # 23
        (0, (length, 100.0, 3000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'city', 'engine')),   # 24
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
        (1, (length, 100.0, 1000.0, 0.0, 0.3, 100.0, 150.0, 0.05, 'speech')),    # 0
        (0, (length, 100.0, 4000.0, 0.2, 0.6, 800.0, 4500.0, 0.05, 'speech')),   # 1
        (0, (length, 100.0, 4000.0, 0.2, 0.4, 1000.0, 4500.0, 0.05, 'speech')),  # 2
        (1, (length, 100.0, 1000.0, 0.0, 0.5, 100.0, 150.0, 0.05, 'speech')),    # 3
        (1, (length, 100.0, 1000.0, 0.0, 0.3, 100.0, 150.0, 0.05, 'speech')),    # 4
        (0, (length, 100.0, 6000.0, 0.1, 0.8, 100.0, 150.0, 0.05, 'speech')),  # 5
        (0, (length, 100.0, 6000.0, 0.1, 0.2, 1400.0, 4500.0, 0.05, 'speech')),  # 6
        (0, (length, 100.0, 6000.0, 0.0, 0.2, 800.0, 4500.0, 0.05, 'speech')),   # 7
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 200.0, 300.0, 0.05, 'speech')),   # 8
        (1, (length, 100.0, 3000.0, 0.0, 0.3, 200.0, 300.0, 0.05, 'speech')),    # 9
        (1, (length, 100.0, 3000.0, 0.0, 0.4, 200.0, 300.0, 0.05, 'speech')),   # 10
        (1, (length, 100.0, 3000.0, 0.0, 0.5, 200.0, 300.0, 0.05, 'speech')),    # 11
        (0, (length, 100.0, 8000.0, 0.2, 0.4, 100.0, 4500.0, 0.05, 'speech')),   # 12
        (0, (length, 100.0, 8000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'speech')),   # 13
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.05, 'speech')),     # 14
        (0, (length, 100.0, 7000.0, 0.2, 0.4, 100.0, 4500.0, 0.05, 'speech')),   # 15
        (0, (length, 100.0, 6000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'speech')),   # 16
        (1, (length, 100.0, 3000.0, 0.0, 0.2, 50.0, 150.0, 0.05, 'speech')),     # 17
        (1, (length, 100.0, 2000.0, 0.0, 0.4, 100.0, 4500.0, 0.05, 'speech')),   # 18
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'speech')),   # 19
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 500.0, 650.0, 0.05, 'speech')),    # 20
        (1, (length, 100.0, 5000.0, 0.0, 0.4, 700.0, 2000.0, 0.01, 'speech')),   # 21
        (0, (length, 100.0, 1000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'speech')),   # 22
        (1, (length, 100.0, 5000.0, 0.0, 0.2, 700.0, 2050.0, 0.01, 'speech')),   # 23
        (0, (length, 100.0, 3000.0, 0.0, 0.2, 100.0, 4500.0, 0.05, 'speech')),   # 24
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
