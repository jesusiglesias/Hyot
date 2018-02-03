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
#        CREATED:     01/21/18                                                                                         #
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
    from RPLCD.i2c import CharLCD                       # Character LCD library
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
sensors = []                                            # Stores the name of all sensors


########################################
#               FUNCTIONS              #
########################################
def init(dht_i2cexpander, dht_i2caddress, hcsr_i2cexpander, hcsr_i2caddress, all_sensors):
    """Initializes as global variables the instances of the LCDs of the sensors
    :param dht_i2cexpander: I2C expander type for LCD 16x2 of the DH11 sensor
    :param dht_i2caddress: I2C address for LCD 16x2 of the DH11 sensor
    :param hcsr_i2cexpander: I2C expander type for LCD 16x2 of the HC-SR04 sensor
    :param hcsr_i2caddress: I2C address for LCD 16x2 of the HC-SR04 sensor
    :param all_sensors: Name of the sensors
    """

    global lcds, dht_lcd, hcsr_lcd, sensors

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing the LCDs " + Style.RESET_ALL)

    try:
        # LCD for the DHT11 sensor. Default 'PCF8574' and 0x3f
        dht_lcd = CharLCD(i2c_expander=dht_i2cexpander,
                          address=int(dht_i2caddress, base=16),
                          charmap='A00',
                          backlight_enabled=False)

        # LCD for the HC-SR04 sensor. Default 'PCF8574' and 0x38
        hcsr_lcd = CharLCD(i2c_expander=hcsr_i2cexpander,
                           address=int(hcsr_i2caddress, base=16),
                           charmap='A00',
                           backlight_enabled=False)

        lcds = [dht_lcd, hcsr_lcd]                      # Instance of all LCDs
        sensors = all_sensors                           # Name of all sensors

        time.sleep(1)
        backlight(True)                                 # Enables the backlight of the LCDs
        time.sleep(2)
        full_print_lcds("Initializing", "HYOT...")      # Prints data in the LCDs using both rows

        print(Fore.GREEN + "        LCDs initialized correctly" + Fore.RESET)

    except IOError as ioError:
        print(Fore.RED + "        Error to initialize the LCDs: " + str(ioError) + ". Main errno:" + "\r")
        print("          - Errno 2: I2C interface is disabled.\r")
        print("          - Errno 22: I2C address is invalid.\r")
        print("          - Errno 121: LCD is not connected.\r")
        sys.exit(1)
    except Exception as lcdError:
        print(Fore.RED + "        Error to initialize the LCDs. Exception: " + Fore.RESET + str(lcdError))
        sys.exit(1)

    time.sleep(2)
    print("\n        ------------------------------------------------------")


def backlight(enabled):
    """Enables or disabled the backlight of all LCDs
    :param enabled: Indicates if the backlight must be enabled or disabled
    """

    global lcds

    for index, lcd in enumerate(lcds):
        lcd.backlight_enabled = enabled

     
def full_print_lcds(first_row, second_row):
    """Writes data in the LCDs using both rows
    :param first_row: Text to write in the first row
    :param second_row: Text to write in the second row
    """

    global lcds

    for index, lcd in enumerate(lcds):
        lcd.write_string(first_row)                     # Writes the specified unicode string to the LCD
        lcd.crlf()                                      # Writes a line feed and a carriage return (\r\n) character
        lcd.write_string(second_row)


def full_print_lcd(sensor, first_row, second_row):
    """Writes data in the specified LCD using both rows
    :param sensor: Indicates the LCD to use based on the sensor
    :param first_row: Text to write in the first row of the specified LCD
    :param second_row: Text to write in the second row of the specified LCD
    """

    global dht_lcd, hcsr_lcd, sensors

    sensor_lcd = None                                   # Stores the LCD instance

    if sensor == sensors[0]:
        sensor_lcd = dht_lcd
    elif sensor == sensors[1]:
        sensor_lcd = hcsr_lcd

    sensor_lcd.write_string(first_row)
    sensor_lcd.crlf()
    sensor_lcd.write_string(second_row)


def print_lcds(dht_data, hcsr_data):
    """Writes data in the LCDs using the first row
    :param dht_data: Text to write in the LCD of the DHT11 sensor
    :param hcsr_data: Text to write in the LCD of the HC-SR04 sensor
    """

    global lcds

    data = [dht_data, hcsr_data]

    for index, lcd in enumerate(lcds):
        lcd.write_string(data[index])                   # Writes the specified unicode string to the LCD


def print_lcd(sensor, data):
    """Writes data in the specified LCD using the first row
    :param sensor: Indicates the LCD to use based on the sensor
    :param data: Text to write in the specified LCD
    """

    global dht_lcd, hcsr_lcd, sensors

    sensor_lcd = None                                   # Stores the LCD instance

    if sensor == sensors[0]:
        sensor_lcd = dht_lcd
    elif sensor == sensors[1]:
        sensor_lcd = hcsr_lcd

    sensor_lcd.write_string(data)


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


def clear_lcd(sensor):
    """Overwrites the LCD of the specified sensor with blank characters and resets the cursor position
    :param sensor: Indicates the LCD to use based on the sensor
    """

    global dht_lcd, hcsr_lcd, sensors

    sensor_lcd = None  # Stores the LCD instance

    if sensor == sensors[0]:
        sensor_lcd = dht_lcd
    elif sensor == sensors[1]:
        sensor_lcd = hcsr_lcd

    sensor_lcd.clear()


def disconnect_lcds():
    """Closes and cleans the LCDs"""

    global lcds, sensors

    for index, lcd in enumerate(lcds):

        print("        Closing and cleaning LCD of the " + sensors[index] + " sensor"),
        time.sleep(0.25)

        try:
            lcd.close(clear=True)                       # Closes and calls the clear function
            lcd.backlight_enabled = False               # Disables the backlight
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
