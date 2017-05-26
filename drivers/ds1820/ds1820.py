#!/usr/bin/python3
"""Driver for the DS1820 temperature sensor.
"""

def read_temperature(address):
    """Parses the special sysfs device and returns the temperature.

    Args:
        address:    the sensor's one-wire bus address
    """
    # Read sysfs file
    path = '/sys/bus/w1/devices/' + address + '/w1_slave'
    try:
        with open(path) as file:
            filecontent = file.read()
    except FileNotFoundError:
        return -1

    # Read and convert
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
    return temperature


if __name__ == '__main__':
    print(read_temperature('10-0008032dcf16'))
