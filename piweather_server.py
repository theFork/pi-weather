#!/usr/bin/python3
"""Pi Weather Server
"""

from flask import Flask, jsonify, render_template, request
from flask import url_for # pylint: disable=unused-import

from database_reader import DatabaseReader
from piweather_config import DATABASE_PATH, VERSION


_APP = Flask(__name__)
_DB = DatabaseReader(DATABASE_PATH, 1000)


@_APP.route('/get_available_timeslot')
def get_available_timeslot():
    """Return a json object containing available timestamp range
    """
    return jsonify(_DB.get_available_timeslot())


@_APP.route('/get_current_humidity')
def get_current_humidity():
    """Returns the current room humidity
    """
    return jsonify(_DB.get_current_humidity())


@_APP.route('/get_current_temperature')
def get_current_temperature():
    """Returns the current room temperature
    """
    return jsonify(_DB.get_current_temperature())


@_APP.route('/get_data')
def get_data():
    """Return a json object containing all data for the specified time slot

    GET-Parameters:
        start:      start timestamp
        end:        end timestamp
    """
    start = request.args.get('start')
    end = request.args.get('end')
    # Read all data available from the database
    (timestamps, brightnesses, humidities, room_temperatures, wall_temperatures) = \
        _DB.fetch_time_slot(start, end)

    # The requested data range has already been read from the DB
    json = jsonify(timestamp=timestamps,
                   brightness=brightnesses,
                   humidity=humidities,
                   room_temperature=room_temperatures,
                   wall_temperature=wall_temperatures)
    return json


@_APP.route('/')
def index():
    """Responds with the rendered page template.
    """
    return render_template('index.html', version=VERSION)


if __name__ == '__main__':
    # Start Flask
    _APP.run(debug=True, host='0.0.0.0')
