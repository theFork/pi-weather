#!/usr/bin/python3
import sqlite3
import time

from drivers.htu21df import HTU21DF as htu21df
from drivers.tsl256x import tsl256x as tsl256x

from piweather import PiWeather

def main():

    # Open database
    db_connection = sqlite3.connect(PiWeather.DATABASE_PATH)
    db_cursor = db_connection.cursor()

    # Add table if necessary
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS weather
                         (timestamp INTEGER, temperature INTEGER, humidity INTEGER, brightness INTEGER)''')

    # Init sensors
    htu21df.htu_reset()
    tsl2560 = tsl256x.TSL256x()

    # Fetch measured values
    temperature = int(htu21df.read_temperature()*100)
    humidity = int(htu21df.read_humidity()*100)
    brightness = tsl2560.lux()
    timestamp = int(time.time())

    # Insert values
    db_cursor.execute('''INSERT INTO weather (timestamp, temperature, humidity, brightness)
                       VALUES (?, ?, ?, ?)''', (timestamp, temperature, humidity, brightness))

    # Save and close
    db_connection.commit()
    db_connection.close()

if __name__ == '__main__':
    main()
