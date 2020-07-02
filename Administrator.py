# ADMINISTRATOR SERVICE
# Austin Dial
# June 21, 2020

# -------------------- CONFIGURE KERNEL -------------------- #

import flask
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
import requests
import sys



# -------------------- DEFINE ROUTE METHODS -------------------- #

@app.route('/api/job', methods=['GET'])
def job():
	# Parse arguments
	if 'configuration' in request.args:
		port = 5000
		job_id = request.args['job_id']
		url = "http://localhost:{}/api/receive_job?job_id={}".format(port, job_id)

		print("Service 2: Received request for job ID {}".format(job_id))
		print("Service 2: Passing request service 1.")

		response = requests.get(url)

		print("Service 2: Received {} response from service.".format(response))
		return "0"

	else:
		print("ERROR Service 2 (broker) Invalid argument received.")
		return "1"



# -------------------- RUN MAIN APP -------------------- #

if __name__ == "__main__":
	if len(sys.argv) >= 3:
		host = sys.argv[1]
		port = sys.argv[2]
		app.run(host=host, port=port, debug=True)
	else:
		print("ERROR Service 2 (main) Invalid number of arguments {}.".format(len(sys.argv)-1))
