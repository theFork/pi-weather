import datetime
import sqlite3
import time

class DatabaseReader:

    def __init__(self, filename):
        self.filename = filename

    def read_last_hours(self, hours=0):
        self.timestamps = []
        self.temperature_values = []
        self.humidity_values = []

        # Open database
        db_con = sqlite3.connect(self.filename)
        db_cur = db_con.cursor()

        # Read all data if hours is zero
        if hours == 0:
            db_cur.execute("SELECT timestamp, temperature, humidity FROM weather")
        else:
            current_timestamp = int(time.time())
            select_timestamp = current_timestamp - (hours * 3600)
            print("Selecting from timestamp " + str(select_timestamp))
            db_cur.execute("SELECT timestamp, temperature, humidity FROM weather WHERE timestamp>=?",
                            (select_timestamp, ))

        for row in db_cur.fetchall():
            self.timestamps.append(datetime.datetime.fromtimestamp(row[0]))
            self.temperature_values.append(row[1] / 100.0)
            self.humidity_values.append(row[2] / 100.0)

        # Close database
        db_con.close()
