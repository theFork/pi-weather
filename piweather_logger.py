#!/usr/bin/python3
"""Polls the sensors and writes one data row to the database.
"""
from sqlite3 import connect
from time import time

from drivers.ds1820 import read_temperature
from drivers.htu21df.HTU21DF import htu_reset, read_humidity
from drivers.tsl256x.tsl256x import TSL256x
from piweather_config import DATABASE_COLUMNS, DATABASE_PATH

def main():
    """Program entry point.
    """
    # Init sensors
    htu_reset()
    tsl2560 = TSL256x()

    # Fetch measured values
    room_temperature = int(read_temperature('10-0008032dcf16'))
    wall_temperature = int(read_temperature('10-0008032dcf14'))
    humidity = int(read_humidity())
    brightness = tsl2560.lux()
    timestamp = int(time())

    # Open database
    db_connection = connect(DATABASE_PATH)
    db_cursor = db_connection.cursor()

    # Add table if necessary
    db_cursor.execute('CREATE TABLE IF NOT EXISTS weather'
                      ' ({} INTEGER,'
                      '  {} INTEGER,'
                      '  {} REAL,'
                      '  {} REAL,'
                      '  {} REAL)'.format(*DATABASE_COLUMNS))

    # Insert values
    query = 'INSERT INTO weather ({}, {}, {}, {}, {}) VALUES (?,?,?,?,?)'.format(*DATABASE_COLUMNS)
    db_cursor.execute(query, (timestamp, brightness, humidity, room_temperature, wall_temperature))

    # Commit transaction and close
    db_connection.commit()
    db_connection.close()

if __name__ == '__main__':
    main()
