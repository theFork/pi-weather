"""Database API
"""
from math import ceil
from datetime import datetime
from sqlite3 import connect

from piweather_config import DATABASE_COLUMNS, DATABASE_NAME, HUMIDITY_COLUMN, ROOM_TEMP_COLUMN, \
                             TIMESTAMP_COLUMN


class DatabaseReader:
    """This class provides an API to read temperature, humidity and brightness data from the
        database.

    Attributes:
        filename        path to the database
        quantity        number of datapoints to fetch
    """
    def __init__(self, filename, quantity):
        self.filename = filename
        self.quantity = quantity


    def _get_latest(self, column):
        """Reads the latest value from the specified column

        Args:
            column      the database column to read from
        """
        with connect(self.filename) as db_con:
            db_cur = db_con.cursor()
            db_cur.execute("SELECT MAX({1}) FROM {0}".format(DATABASE_NAME, TIMESTAMP_COLUMN))
            latest_timestamp = db_cur.fetchone()[0]
            print("{} :: {} ".format(latest_timestamp, type(latest_timestamp)))
            query = "SELECT {1} FROM {0} WHERE {2} = ?"
            query = query.format(DATABASE_NAME, column, TIMESTAMP_COLUMN)
            db_cur.execute(query, (latest_timestamp,))
            return db_cur.fetchone()[0]


    def fetch_time_slot(self, start, end):
        """Reads temperature, humidity and brightness data in the specified time slot.

        Args:
            start       timestamp to start from
            end         latest timestamp to read

        Returns:
            (timestamps, brightness_values, humidity_values, room_temperature_values, \
             wall_temperature_values)
        """
        timestamps = []
        brightness_values = []
        humidity_values = []
        room_temperature_values = []
        wall_temperature_values = []

        with connect(self.filename) as db_con:
            db_cur = db_con.cursor()

            # Count data points and compute row skip
            query = "SELECT COUNT(*) FROM {0}"
            query += " WHERE ? <= {1} AND {1} <= ?"
            db_cur.execute(query.format(DATABASE_NAME, TIMESTAMP_COLUMN), (start, end))
            skip = ceil(db_cur.fetchone()[0] / self.quantity)

            # Read data using time filter and row skip
            query = "SELECT {1}, {2}, {3}, {4}, {5} FROM {0}"
            query += " WHERE ? <= {1} AND {1} <= ?"
            query += " AND rowid % ? = 0"
            db_cur.execute(query.format(DATABASE_NAME, *DATABASE_COLUMNS), (start, end, skip))

            # Re-pack data to tuple of arrays
            for row in db_cur.fetchall():
                timestamps.append(datetime.fromtimestamp(row[0]))
                brightness_values.append(row[1])
                humidity_values.append(row[2])
                room_temperature_values.append(row[3])
                wall_temperature_values.append(row[4])

        return (timestamps, brightness_values, humidity_values, room_temperature_values, \
                wall_temperature_values)


    def get_available_timeslot(self):
        """Returns the first and last timestamp from the database.

        Returns:
            (min_timestamp, max_timestamp)
        """
        with connect(self.filename) as db_con:
            db_cur = db_con.cursor()
            db_cur.execute("SELECT MIN({1}) FROM {0}".format(DATABASE_NAME, TIMESTAMP_COLUMN))
            min_timestamp = db_cur.fetchone()[0]
            db_cur.execute("SELECT MAX({1}) FROM {0}".format(DATABASE_NAME, TIMESTAMP_COLUMN))
            max_timestamp = db_cur.fetchone()[0]
        result = dict()
        result['start'] = min_timestamp
        result['end'] = max_timestamp
        return result


    def get_current_humidity(self):
        """Reads the latest room humidity from the database

        Returns:
            (uint) the current humidity
        """
        return self._get_latest(HUMIDITY_COLUMN)


    def get_current_temperature(self):
        """Reads the latest room temperature from the database

        Returns:
            (float) the current temperature
        """
        return self._get_latest(ROOM_TEMP_COLUMN)
