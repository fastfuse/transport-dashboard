from app import app
from flask import render_template, jsonify, make_response
import csv
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    with open('stops.txt', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        collection = {"type": "FeatureCollection"}
        features = []

        for row in reader:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row.pop('stop_lon'), row.pop('stop_lat')],
                },
                "properties": row
            }

            features.append(feature)

        collection['features'] = features

        with open('data.json', 'w') as f:
            json.dump(collection, f)

    return make_response(jsonify(collection)), 200
