import datetime
import sqlite3
import time

class DatabaseReader:
    QUERY = "SELECT timestamp, temperature/100.0, humidity/100.0, brightness FROM weather"

    def __init__(self, filename):
        self.filename = filename

    def read_last_hours(self, hours=0):
        self.timestamps = []
        self.temperature_values = []
        self.humidity_values = []
        self.brightness_values = []

        # Open database
        db_con = sqlite3.connect(self.filename)
        db_cur = db_con.cursor()

        # Read all data if hours is zero
        if hours == 0:
            db_cur.execute(self.QUERY)
        else:
            current_timestamp = int(time.time())
            select_timestamp = current_timestamp - (hours * 3600)
            print("Selecting from timestamp " + str(select_timestamp))
            db_cur.execute(self.QUERY + "WHERE timestamp>=?", (select_timestamp, ))

        # TODO: This appears quiet inefficient
        for row in db_cur.fetchall():
            self.timestamps.append(datetime.datetime.fromtimestamp(row[0]))
            self.temperature_values.append(row[1])
            self.humidity_values.append(row[2])
            self.brightness_values.append(row[3])

        # Close database
        db_con.close()
