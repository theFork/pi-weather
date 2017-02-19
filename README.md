# PI-WEATHER
A simplistic indoor climate logger application for the Raspberry Pi.

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

6. Reboot

# Using Arch for development
For those who prefer Arch Linux, a development environment can be set up as follows:

```bash
sudo yaourt -Suy python3 pip3
sudo pip3 install flask
```
