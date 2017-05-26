"""This module defines common constants and offers an interface for configuring connected sensors
"""

VERSION = '0.3.1'
DATABASE_PATH = 'weather.db'

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
