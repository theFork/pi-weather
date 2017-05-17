#!/usr/bin/python3
"""Polls the sensors and writes one data row to the database.
"""
from sqlite3 import connect
from time import time

from drivers.htu21df.HTU21DF import htu_reset, read_humidity, read_temperature
from drivers.tsl256x.tsl256x import TSL256x
from piweather_config import DATABASE_PATH

def main():
    """Program entry point.
    """
    # Init sensors
    htu_reset()
    tsl2560 = TSL256x()

    # Fetch measured values
    temperature = int(read_temperature() * 100)
    humidity = int(read_humidity() * 100)
    brightness = tsl2560.lux()
    timestamp = int(time())

    # Open database
    db_connection = connect(DATABASE_PATH)
    db_cursor = db_connection.cursor()

    # Add table if necessary
    db_cursor.execute('CREATE TABLE IF NOT EXISTS weather'
                      ' (timestamp   INTEGER,'
                      '  temperature INTEGER,'
                      '  humidity    INTEGER,'
                      '  brightness  INTEGER)')

    # Insert values
    db_cursor.execute('INSERT INTO weather (timestamp, temperature, humidity, brightness)'
                      '             VALUES (        ?,           ?,        ?,          ?)',
                      (timestamp, temperature, humidity, brightness))

    # Commit transaction and close
    db_connection.commit()
    db_connection.close()

if __name__ == '__main__':
    main()
