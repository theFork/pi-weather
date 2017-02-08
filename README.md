# PI-WEATHER
A simplistic indoor climate logger application for the Raspberry Pi.

# Setting up Raspbian live system
After installing a recent version of Raspbian on the Pi, take the following steps:

1. Activate I2C via raspi-config
2. Install required dependencies:

```bash
sudo apt-get install python3 python3-pigpio python3-pip python3-flask python3-matplotlib
sudo pigpiod

```

3. Start the pigpio deamon

```
sudo pigpiod
```

# Using Arch for development
For those who prefer Arch Linux, a development environment can be set up as follows:

```bash
sudo yaourt -Suy python3 pip3
sudo pip3 install flask matplotlib
```
