#!/usr/bin/python
# -*- coding: utf-8 -*-
# =====================================================================================================================#
#                                                                                                                      #
#                                    __    __   ___      ___   ________    __________                                  #
#                                   |  |  |  |  \  \    /  /  |   __   |  |___    ___|                                 #
#                                   |  |__|  |   \  \__/  /   |  |  |  |      |  |                                     #
#                                   |   __   |    \_|  |_/    |  |  |  |      |  |                                     #
#                                   |  |  |  |      |  |      |  |__|  |      |  |                                     #
#                                   |__|  |__|      |__|      |________|      |__|                                     #
#                                                                                                                      #
#                                                                                                                      #
#        PROJECT:     Hyot                                                                                             #
#           FILE:     raspberrypi_hyot.py                                                                              #
#                                                                                                                      #
#          USAGE:     python raspberrypi_hyot.py                                                                       #
#                                                                                                                      #
#    DESCRIPTION:     This script monitors several events from sensors and sends them to the cloud  TODO               #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Root user, Connected devices: 16x2 LCD (2), DTH11 sensor and HC-SR04 sensor                      #
#          NOTES:     It must be run with root user on a Raspberry Pi preferably with Raspbian as operating system     #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     12/27/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This script monitors several events from sensors and sends them to the cloud"""  # TODO

########################################
#               IMPORTS                #
########################################
from __future__ import unicode_literals
import os
import sys
import time
import datetime
import Adafruit_DHT                             # DHT11 sensor
from RPLCD.i2c import CharLCD                   # LCD 16x2


########################################
#              CONSTANTS               #
########################################
def constants():
    """Contains all definitions of constants"""

    global LCD, DHT_SENSOR, DHT_PINDATA

    LCD = CharLCD(i2c_expander='PCF8574', address=0x3f, charmap='A00')      # LCD 16x2 - Configurable I2C address
    DHT_SENSOR = Adafruit_DHT.DHT11                                         # DHT11 sensor
    DHT_PINDATA = 21                                                        # DHT11 - Pin GPIO21


########################################
#               FUNCTIONS              #
########################################
def check_root():
    """Check that the script is run as a root user"""

    if not os.geteuid() == 0:
        print("You need to have root privileges to run this script. Please try again, this time using 'sudo'.")
        sys.exit(1)


def main():
    """Main function"""

    # Try-Catch block
    try:

        # Initializing
        print("Initializing Raspberry Pi")
        LCD.write_string("Initializing")            # Writes the specified unicode string to the display
        LCD.crlf()                                  # Writes a line feed and a carriage return (\r\n) character
        LCD.write_string("Raspberry Pi...")
        time.sleep(3)                               # Wait time - 3 seconds
        LCD.clear()                                 # Overwrites display with blank characters and reset cursor position

        # Reading values
        print("Reading values from sensors")
        LCD.write_string("Reading values")
        LCD.crlf()
        LCD.write_string("from sensors")
        time.sleep(2)
        LCD.clear()

        # DHT11 sensor TODO
        LCD.write_string("-> DHT11 sensor")
        time.sleep(2)
        LCD.clear()

        # Loop each 3 seconds, hence, this is the time between measurements
        while True:

            # Obtains humidity and temperature from DHT11 sensor
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PINDATA)
            # Obtains the datetime
            measure_datetime = datetime.datetime.now()

            # Checks the values
            if humidity is not None and 0 <= humidity <= 100 and temperature is not None and temperature >= 0:

                # Outputs the data by console
                print("Datetime of measurement: " + str(measure_datetime.strftime("%d-%m-%Y %H:%M:%S %p")))

                print("Temperature: {0:0.1f} °C \nHumidity: {1:0.1f} %".format(temperature, humidity))

                # Outputs the data by display
                LCD.cursor_pos = (0, 0)
                LCD.write_string("Temp: %.1f °C" % temperature)
                LCD.crlf()
                LCD.write_string("Humidity: %.1f %%" % humidity)

            elif humidity is None or 0 > humidity > 100:                            # Humidity value invalid or None
                print ("Failed to get reading. Humidity is invalid or None")

            elif temperature is None or temperature < 0:                            # Temperature value invalid or None
                print ("Failed to get reading. Temperature is invalid or None")

            time.sleep(3)

    except Exception as error:                          # TODO - Too general exception
        print ("Error: " + str(error) + "\r")
    except KeyboardInterrupt:
        print ("\r")
    finally:
        LCD.close(clear=True)                           # Close and call the clear function
        LCD.backlight_enabled = False                   # Disable the backlight


########################################
#             MAIN PROGRAM             #
########################################
if __name__ == '__main__':

    check_root()                # Function to check the user
    constants()                 # Declares all the constants
    main()                      # Main function
