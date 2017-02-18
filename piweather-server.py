#!/usr/bin/python3

from flask import Flask, jsonify, redirect, render_template, request, make_response, url_for

import datetime, time
from io import BytesIO

from database_reader import DatabaseReader
from piweather import PiWeather

app = Flask(__name__)
db = DatabaseReader(PiWeather.DATABASE_PATH)


@app.route('/')
def index():
    # Read all data available from the database
    db.read_last_hours()
    return render_template('index.html', version=PiWeather.VERSION)


@app.route('/range_select_action', methods=['POST'])
def plot_range():
    # Examine integer entered (empty equals 0)
    form_content = request.form['hours']
    if form_content == '':
        hours_to_display = 0
    else:
        hours_to_display = int(request.form['hours'])

    # Read only data requested
    start_time = time.time()
    db.read_last_hours(hours_to_display)
    duration_ms = (time.time() - start_time) * 1000
    print('DB read duration: %.2f ms' % duration_ms)

    return render_template('index.html', version=PiWeather.VERSION)


@app.route('/get_data')
def get_data():
    # The requested data range has already been read from the DB
    json = jsonify(timestamp=db.timestamps,
                   temperature=db.temperature_values,
                   humidity=db.humidity_values,
                   brightness=db.brightness_values)
    print(json)
    return json


if __name__ == '__main__':
    # Start Flask
    app.run(debug=True, host='0.0.0.0')
