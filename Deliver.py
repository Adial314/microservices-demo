# DELIVER
# Austin Dial
# June 21, 2020

# -------------------- CONFIGURE KERNEL -------------------- #

import flask
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)



# -------------------- DEFINE ROUTE METHODS -------------------- #

@app.route('/api/receive_job', methods=['GET'])
def receive_job():
	# Parse arguments
	if 'job_id' in request.args:
		job_id = request.args['job_id']
		print("Service 1: Received request for job ID {}.".format(job_id))
		return "0"
	else:
		print("ERROR Service 1 (request) Invalid argument received.")
		return "1"



# -------------------- RUN MAIN APP -------------------- #

if __name__ == "__main__":
	app.run(host= '0.0.0.0', debug=True)
