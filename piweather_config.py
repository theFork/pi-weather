"""This module defines common constants and offers an interface for configuring connected sensors
"""

VERSION = '0.4.0'
DATABASE_PATH = '/home/haggl/weather.db'

BRIGHTNESS_COLUMN = 'brightness'
TIMESTAMP_COLUMN = 'timestamp'
HUMIDITY_COLUMN = 'humidity'
ROOM_TEMP_COLUMN = 'room_temp'
WALL_TEMP_COLUMN = 'wall_temp'
DATABASE_COLUMNS = tuple([TIMESTAMP_COLUMN,  \
                         BRIGHTNESS_COLUMN, \
                         HUMIDITY_COLUMN,   \
                         ROOM_TEMP_COLUMN,  \
                         WALL_TEMP_COLUMN])

ROOM_TEMP_ADDR = '10-0008032dcf16'
WALL_TEMP_ADDR_0 = '10-0008032dc6ae'
WALL_TEMP_ADDR_1 = '10-0008032dc0b6'
