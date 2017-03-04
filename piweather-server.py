#!/usr/bin/python3
"""Pi Weather Server
"""

from flask import Flask, jsonify, render_template

#import datetime, time
#from io import BytesIO

from database_reader import DatabaseReader
from piweather import PiWeather

_APP = Flask(__name__)
_DB = DatabaseReader(PiWeather.DATABASE_PATH, 1000)


@_APP.route('/')
def index():
    """Responds with the rendered page template.
    """
    return render_template('index.html', version=PiWeather.VERSION)

@_APP.route('/get_data')
def get_data():
    """Fetch data TODO
    """
    # Read all data available from the database
    (timestamps, temperature_values, humidity_values, brightness_values) = _DB.fetch_time_slot()

    # The requested data range has already been read from the DB
    json = jsonify(timestamp=timestamps,
                   temperature=temperature_values,
                   humidity=humidity_values,
                   brightness=brightness_values)
    print(json)
    return json


if __name__ == '__main__':
    # Start Flask
    _APP.run(debug=True, host='0.0.0.0')
