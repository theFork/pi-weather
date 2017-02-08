#!/usr/bin/python3

from flask import Flask, redirect, render_template, request, make_response, url_for

import datetime
from io import BytesIO

from database_reader import DatabaseReader
from piweather import PiWeather

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib import style

# Mathplotlib style
style.use('ggplot')

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
    db.read_last_hours(hours_to_display)

    return render_template('index.html', version=PiWeather.VERSION)

@app.route('/plot.png')
def plot_full_image():

    # The requested data range has already been red from the DB

    # Create figure
    fig = Figure()
    temp_ax=fig.add_subplot(111)
    hum_ax = temp_ax.twinx()

    # Define plots
    temp_ax.plot_date(db.timestamps, db.temperature_values, 'r-')
    hum_ax.plot_date(db.timestamps, db.humidity_values, 'b-')

    # Format x-axis
    temp_ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
    fig.autofmt_xdate()

    # Format and label y-axes
    temp_ax.set_ylabel('T [°C]', color='r')
    temp_ax.tick_params('y', colors='r')
    hum_ax.set_ylabel('Rel. Hum. [%]', color='b')
    hum_ax.tick_params('y', colors='b')

    # Plot and return PNG
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == '__main__':
    # Start Flask
    app.run(debug=True, host='0.0.0.0')
