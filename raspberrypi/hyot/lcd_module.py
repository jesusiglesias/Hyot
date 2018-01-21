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
#           FILE:     lcd_module.py                                                                                    #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to handle the LCDs                                                #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Connected devices: LCD 16x2 (2)                                                                  #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/21/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic to handle the LCDs"""

########################################
#               IMPORTS                #
########################################
from __future__ import unicode_literals                 # Future statement definitions

try:
    import sys                                          # System-specific parameters and functions
    import time                                         # Time access and conversions
    from colorama import Fore, Style                    # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in lcd_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
dht_lcd = None                                          # Instance of the LCD of the DHT11 sensor
hcsr_lcd = None                                         # Instance of the LCD of the HC-SR04 sensor
lcds = []                                               # Stores the instances of all sensors
sensors = []                                            # Stores tne name of all sensors


########################################
#               FUNCTIONS              #
########################################
def init(dht, hcsr, all_sensors):
    """Initializes as global variables the instances of the LCDs of the sensors
    :param dht: Instance of the LCD of the DHT11 sensor
    :param hcsr: Instance of the LCD of the HC-SR04 sensor
    :param all_sensors: Name of the sensors
    """

    global lcds, dht_lcd, hcsr_lcd, sensors

    dht_lcd = dht                                   # LCD of the DHT11 sensor
    hcsr_lcd = hcsr                                 # LCD of the HC-SR04 sensor
    lcds = [dht_lcd, hcsr_lcd]                      # Instance of all LCDs
    sensors = all_sensors                           # Name of all sensors


def backlight(enabled):
    """Enables or disabled the backlight of all LCDs
    :param enabled: Indicates if the backlight must be enabled or disabled
    """

    for index, lcd in enumerate(lcds):
        lcd.backlight_enabled = enabled

     
def full_print_lcds(first_row, second_row):
    """Writes data in the LCDs using both rows
    :param first_row: Text to write in the first row
    :param second_row: Text to write in the second row
    """

    global lcds, dht_lcd, hcsr_lcd

    for index, lcd in enumerate(lcds):
        lcd.write_string(first_row)                 # Writes the specified unicode string to the LCD
        lcd.crlf()                                  # Writes a line feed and a carriage return (\r\n) character
        lcd.write_string(second_row)


def print_lcds(dht_data, hcsr_data):
    """Writes data in the LCDs using the first row
    :param dht_data: Text to write in the LCD of the DHT11 sensor
    :param hcsr_data: Text to write in the LCD of the HC-SR04 sensor
    """

    global lcds, dht_lcd, hcsr_lcd

    data = [dht_data, hcsr_data]

    for index, lcd in enumerate(lcds):
        lcd.write_string(data[index])               # Writes the specified unicode string to the LCD


def print_measure_dht(temperature, humidity, error_measure, clear_lcd):
    """Writes in the LCD of the DHT11 sensor the values of each measure
    :param temperature: Value of the temperature event
    :param humidity: Value of the humidity event
    :param error_measure: Indicates if the current measurement is valid
    :param clear_lcd: Indicates if the LCD must be cleared
    """

    global dht_lcd

    if clear_lcd:
        dht_lcd.clear()                                         # Clears the LCD

    dht_lcd.cursor_pos = (0, 0)                                 # Establishes the cursor in the initial position
    if not error_measure:
        dht_lcd.write_string("Temp: %.1f °C" % temperature)     # Writes the specified unicode string to the LCD
    else:
        dht_lcd.write_string("Temp: ")

    dht_lcd.crlf()                                              # Writes a line feed and a carriage return character

    if not error_measure:
        dht_lcd.write_string("Humidity: %.1f %%" % humidity)
    else:
        dht_lcd.write_string("Humidity: ")


def clear_lcds():
    """Overwrites both LCDs with blank characters and resets the cursor position"""

    global lcds

    for index, lcd in enumerate(lcds):
        lcd.clear()


def disconnect_lcds():
    """Closes and cleans the LCDs"""

    global lcds

    for index, lcd in enumerate(lcds):

        print("        Closing and cleaning LCD of the " + sensors[index] + " sensor"),
        time.sleep(0.25)

        try:
            lcd.close(clear=True)                   # Closes and calls the clear function
            lcd.backlight_enabled = False           # Disables the backlight
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
