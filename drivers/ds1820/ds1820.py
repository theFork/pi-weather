#!/usr/bin/python3

def get_temperature(address):
    # Read sysfs file
    path = '/sys/bus/w1/devices/' + address + '/w1_slave'
    with open(path) as file:
        filecontent = file.read()

    # Read and convert
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
    return temperature


if __name__ == '__main__':
    temp = get_temperature('10-0008032dcf16')
    print(temp)
