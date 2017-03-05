"""Database API
"""
import datetime
import sqlite3

class DatabaseReader:
    """This class provides an API to read temperature, humidity and brightness data from the
        database.
    """
    _QUERY = "SELECT timestamp, temperature/100.0, humidity/100.0, brightness FROM weather"

    def __init__(self, filename, quantity):
        """Constructs a DatabaseReader.

        Args:
            filename    path to the database
            quantity    number of datapoints to fetch
        """
        self.filename = filename
        self.quantity = quantity

    def fetch_time_slot(self, start=0, end=0):
        """Reads temperature, humidity and brightness data in the specified time slot.

        Args:
            start       timestamp to start from
            end         latest timestamp to read

        Returns:
            (timestamps, temperature_values, humidity_values, brightness_values)
        """
        timestamps = []
        temperature_values = []
        humidity_values = []
        brightness_values = []

        # Open database
        db_con = sqlite3.connect(self.filename)
        db_cur = db_con.cursor()

        # Read all data if not timestamps were provided
        if start == 0 and end == 0:
            db_cur.execute(self._QUERY)
        else:
            db_cur.execute(self._QUERY + " WHERE ?<=timestamp AND timestamp<=?", (start, end))

        for row in db_cur.fetchall():
            timestamps.append(datetime.datetime.fromtimestamp(row[0]))
            temperature_values.append(row[1])
            humidity_values.append(row[2])
            brightness_values.append(row[3])

        # Close database
        db_con.close()

        return (timestamps, temperature_values, humidity_values, brightness_values)


    def get_available_timeslot(self):
        """Returns the first and last timestamp from the database.

        Returns:
            (min_timestamp, max_timestamp)
        """
        db_con = sqlite3.connect(self.filename)
        db_cur = db_con.cursor()
        db_cur.execute("SELECT MIN(timestamp) FROM weather")
        min_timestamp = db_cur.fetchone()[0]
        db_cur.execute("SELECT MAX(timestamp) FROM weather")
        max_timestamp = db_cur.fetchone()[0]
        db_con.close()
        return (min_timestamp, max_timestamp)
