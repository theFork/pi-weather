# PI-WEATHER
A simplistic indoor climate logger application for the Raspberry Pi.

# Wiring
This is the pinout of a Raspberry Pi 1 Model B:

| Phys. Pin | Used as              |
| --------- | -------------------- |
| 1         | 3,3V
| 2         | 5V
| 3         | SDA (BCM2)
| 4         | 5V
| 5         | SCL (BCM3)
| 6         | GND
| 7         | 1-Wire (BCM4)
| 8         | (BCM14)
| 9         | GND
| 10        | (BCM15)

## DS1820
Add a 4.7k resistor between 3,3V and BCM4.

# Setting up Raspbian live system
After installing a recent version of Raspbian on the Pi, take the following steps:

1. Activate I2C via raspi-config
2. Install required dependencies:

    ```bash
    sudo apt-get install python3 python3-pigpio python3-pip python3-flask
    sudo pigpiod
    ```

3. Start the pigpio deamon

    ```
    sudo pigpiod
    ```

4. Set up a cron job. As your user (we are assuming pi here), run

    ```
    crontab -e
    ```

    and append the following line


    ```
    * * * * * cd /home/pi/repositories/pi-weather/ && ./piweather-logger.py
    ```
    . This should run the logger every minute.

5. Start pigpiod and piweather-server at startup. Lazy people can do this also using cron:

    ```
    sudo crontab -e
    ```

    Insert these lines:

    ```
    @reboot /usr/bin/pigpiod
    @reboot cd /home/pi/repositories/pi-weather && ./piweather-server.py
    ```

5. For enabling 1-Wire communication with DS1820 sensors, append the following lines to /boot/config.txt:

    ```
    # DS1820
    dtoverlay=w1-gpio, gpiopin=4
    ```

After rebooting, you should be able to read the sensors via sysfs.

6. Reboot

# Using Arch for development
For those who prefer Arch Linux, a development environment can be set up as follows:

```bash
sudo yaourt -Suy python3 pip3
sudo pip3 install flask
```
