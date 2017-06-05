#!/usr/bin/python3
"""Polls the sensors and writes one data row to the database.
"""
from sqlite3 import connect
from time import time

from drivers.ds1820 import read_temperature
from drivers.htu21df.HTU21DF import htu_reset, read_humidity
from drivers.tsl256x.tsl256x import TSL256x
from piweather_config import DATABASE_COLUMNS, DATABASE_NAME, DATABASE_PATH, \
                             ROOM_TEMP_ADDR, WALL_TEMP_ADDR_0, WALL_TEMP_ADDR_1

def main():
    """Program entry point.
    """
    # Init sensors
    htu_reset()
    tsl2560 = TSL256x()

    # Fetch room temperature
    room_temperature = read_temperature(ROOM_TEMP_ADDR)

    # Read two wall-sensors and store minimum
    wall_temperature = min(read_temperature(WALL_TEMP_ADDR_0), read_temperature(WALL_TEMP_ADDR_1))

    # Read humidity and brightness
    humidity = int(read_humidity())
    brightness = tsl2560.lux()

    # Generate timestamp
    timestamp = int(time())

    with connect(DATABASE_PATH) as db_connection:
        db_cursor = db_connection.cursor()

        # Add table if necessary
        db_cursor.execute('CREATE TABLE IF NOT EXISTS {}'
                          ' ({} INTEGER,'
                          '  {} INTEGER,'
                          '  {} REAL,'
                          '  {} REAL,'
                          '  {} REAL)'.format(DATABASE_NAME, *DATABASE_COLUMNS))

        # Insert values
        query = 'INSERT INTO {} ({}, {}, {}, {}, {}) VALUES (?,?,?,?,?)'
        db_cursor.execute(query.format(DATABASE_NAME, *DATABASE_COLUMNS),
                          (timestamp, brightness, humidity, room_temperature, wall_temperature))
        db_connection.commit()


if __name__ == '__main__':
    main()
