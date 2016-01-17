from flask import Flask, jsonify, request
import requests
import json
from flask.ext.cors import CORS, cross_origin
import time


import rethinkdb as r

conn = r.connect( "localhost", 28015, db='heck')


app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route('/')
@cross_origin(origin='*')
def hello():
	return "hello world"

@app.route('/beacons', methods=['POST'])
@cross_origin(origin='*')
def beacons():
	bname = request.form['beaconname']
	buid  = request.form['buid']
	brssi = request.form['rssi']

	data = [{
		"name" : bname,
		"uid"  : buid,
		"rssi":  int(brssi),
		"timestamp": time.time()
	}]
#TODO CHANGE THIS TO GET THEN REPLACE
	r.table('beacons').insert(data,  conflict="replace").run(conn)

	return 'Success!'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8521)