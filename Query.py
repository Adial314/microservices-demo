# QUERY SERVICE
# Austin Dial
# June 21, 2020

# -------------------- CONFIGURE KERNEL -------------------- #

import flask
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

from lib import sqltools as sqlt



# -------------------- SQLITE METHODS -------------------- #

def sqlite_connect(database):
	"""Returns connection object to specified database."""
	return sqlt.database_connection(database)


def sqlite_query(connection, query):
	"""Returns the results of a specified query against a specified database connection."""
	print("SQL Query: {}".format(query))
	cursor = connection.cursor()
	cursor.execute(query)
	return cursor.fetchall()


def sqlite_columns(connection, table):
	"""Returns the column names of the specified table in the specified database."""

	# Query table names
	query = "pragma table_info('%s');" % table
	print("SQL Query: {}".format(query))
	cursor = connection.cursor()
	cursor.execute(query)
	results = cursor.fetchall()

	# Parse names from resultset
	columns = list([])
	for tupl in results:
		columns.append(tupl[1])

	return columns



# -------------------- CONVERSION METHODS -------------------- #

def list_of_tuples(lot, keys=None):
	"""Returns an object-based JSON formatted file from a list of tuples."""
	
	# Define default keys if they are not supplied
	if not keys:
		keys = list([])
		for i in range(len(lot[0])):
			field = "field" + str(i)
			keys.append(field)

	# Iterate through each tuple in the list
	objects = list([])
	for entry in lot:
	    # Aggregate values from tuple
	    values = list([])
	    for value in entry:
	        values.append(value)
	    # Form dictionary from keys and values lists
	    obj = dict(zip(keys, values))
	    # Append object to objects list
	    objects.append(obj)
	values_copy = values
	# Form final objects-based dictionary
	return dict({"objects": objects})



# -------------------- DEFINE ROUTES -------------------- #

@app.route('/api/receive', methods=['GET'])
def receive():
	# Parse arguments
	source    = request.args.get('source')
	database  = request.args.get('database')
	username  = request.args.get('username')
	password  = request.args.get('password')
	table     = request.args.get('table')
	path      = request.args.get('path')

	# SQLite3 protocol
	if source == 'sqlite':
		# Open and execute query
		queryFile = open(path, 'r')
		query     = queryFile.read()
		queryFile.close()
		conn      = sqlite_connect(database)
		results   = sqlite_query(conn, query)

		# Capture table keys
		keys = sqlite_columns(conn, "accounts")

		# Return processed data
		return list_of_tuples(results, keys)


	# Default protocol
	else:
		return "Connection protocol not defined."



# -------------------- RUN MAIN APP -------------------- #

if __name__ == "__main__":
	app.run(host= '0.0.0.0', debug=True)
