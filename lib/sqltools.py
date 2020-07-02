# -------------------- CONFIGURE KERNEL -------------------- #

import sqlite3
from sqlite3 import Error
import json
import os
import pandas as pd


# -------------------- DEFINE FUNCTIONS -------------------- #

def database_connection(database, verbosity=0):
    """Create a connection to SQLite database. If the database does not exist then it will be created.
    Returns the connection object.
    """

    # Verbose output
    if verbosity != 0:
        print("Connecting to database: {}.".format(database))

    # Attempt to connect to database
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as error:
        print(error)

    # Return results
    if conn:
        if verbosity != 0:
            print("Connection successful.")
        return conn
    else:
        if verbosity != 0:
            print("Connection was not successful.")
        return None


def execute_query(connection, query, verbosity=0):
    """Execute a given query against a given database connection.
    Returns 1 on success, 0 on failure.
    """

    # Verbose output
    if verbosity == 2:
            print("Executing query: ")
            print(query)

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.commit()
        return 1
    except Error as error:
        print(error)
        return 0


def create_table(connection, configuration, verbosity=0):
    """Dynamically create a table in the supplied database.
    Requires a dictionary object describing the table characteristics.
    Returns 1 on success, 0 on failure.
    """
    
    # Communicate
    if verbosity != 0:
        print("Creating {} table.".format(configuration['name']))

    # Start query string
    query = "CREATE TABLE IF NOT EXISTS {} (".format(configuration['name'])

    # Iteratively format column specification
    # Add the columns to the query individually 
    for column in configuration['columns']:
        # Format column specification
        specification = " {} {}".format(column['name'], column['type'])
        if not column['null']:
            specification += " NOT NULL"
        if column['primary_key']:
            specification += " PRIMARY KEY"
        specification += ","

        # Add column specification to query
        query += specification

    # Finish query
    query = query[:-1]
    query += " )"
	
    # Execute query
    result = execute_query(connection, query)
        
    # Return result
    return result


def populate_table(connection, configuration, verbosity=0):
    """Dynamically populates a table in the supplied database based on the table configuration.
    Requires a database connection and a dictionary object describing the table configuration.
    Returns 1 on success, 0 on failure.
    """
    
    # Read CSV dataset
    data = pd.read_csv(configuration['data'])

    # Parse out table name
    table = configuration['name']

    # Parse out column names
    columns = ""
    for column in configuration['columns']:
        columns += str(column['name']) + ", "
    columns = columns[0:-2]
    
    # Communicate
    if verbosity != 0:
        print("Populating {} table.".format(table))

    # Iteratively form and execute queries
    for index, row in data.iterrows():

        # Parse out values into CSV string
        values = ""
        for value in row.values:
            if type(value) == int:
                values += str(value) + ", "
            elif type(value) == str:
                values += "'" + str(value) + "', "
        values = values[0:-2]

        # Form insert query
        query = "INSERT INTO {}({}) VALUES({})".format(table, columns, values)

        # Execute insert query with error handling
        result = execute_query(connection, query, verbosity)
        
    # Return successful result
    return 1

