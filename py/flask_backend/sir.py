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

@app.route('/position', methods=['POST'])
@cross_origin(origin='*')
def position():
	s = request.form['segment']
	x = request.form['x']
	y = request.form['y']
	data = [{
		"uid" : 0,
		"segment" : s,
		"x": x,
		"y": y
	}]
#TODO CHANGE THIS TO GET THEN REPLACE
	r.table('position').insert(data,  conflict="replace").run(conn)

	return 'Success!'

@app.route('/where', methods=['GET'])
@cross_origin(origin='*')
def where():

	cursor = r.table("position").run(conn)
	#cursor = r.table("beacons").delete().run(conn)
	for document in cursor:
	    x = document

	segment_mapping = {-1:"Please try again!", 0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9"}
	
	html = "<body style = 'text-align: center;font-size: 6em;'>" + segment_mapping[int(x["segment"])] + "<br><img src='../sim/wo/plot.png'></body>"

	return html

@app.route('/wherej', methods=['GET'])
@cross_origin(origin='*')
def wherej():

	cursor = r.table("position").run(conn)
	#cursor = r.table("beacons").delete().run(conn)
	for document in cursor:
	    x = document

	Json = "{'segment': "+ str(int(x["segment"])) + "}"

	return Json

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8521)