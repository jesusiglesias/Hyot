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
from __future__ import unicode_literals             # Future statement definitions

try:
    import sys                                      # System-specific parameters and functions
    import os                                       # OS module
    import re                                       # Regular expression
    import uuid                                     # UUID objects according to RFC 4122
    import time                                     # Time access and conversions
    import datetime                                 # Basic date and time types
    import psutil                                   # Python system and process utilities
    from pyfiglet import Figlet                     # Text banners in a variety of typefaces
    from colorama import Fore, Style                # Cross-platform colored terminal text
    import Adafruit_DHT                             # DHT11 sensor
    from RPLCD.i2c import CharLCD                   # LCD 16x2

except ImportError as importError:
    print("Error to import: " + importError.message.lower())
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
def constants():
    """Contains all definitions of constants"""

    global FIGLET, LCD, DHT_SENSOR, DHT_PINDATA

    FIGLET = Figlet(font='future_8', justify='center')                  # Figlet
    LCD = CharLCD(i2c_expander='PCF8574',                               # LCD 16x2 - Configurable I2C address
                  address=0x3f,
                  charmap='A00',
                  backlight_enabled=False)
    DHT_SENSOR = Adafruit_DHT.DHT11                                     # DHT11 sensor
    DHT_PINDATA = 21                                                    # DHT11 - Pin GPIO21


########################################
#               FUNCTIONS              #
########################################
def check_root():
    """Checks that the script is run as a root user"""

    if not os.geteuid() == 0:
        print(Fore.RED + "You need to have root privileges to run this script. Please try it again using 'sudo'." + Fore.RESET)
        sys.exit(1)


def check_platform():
    """Checks that the script is run on GNU/Linux platform"""

    if not sys.platform.startswith('linux'):
        print(Fore.RED + "This script must be run on GNU/Linux platform. For example: Raspbian." + Fore.RESET)
        sys.exit(1)


def check_raspberrypi():
    """Checks that the script is run on Raspberry Pi. Opens the '/proc/cpuinfo' file to obtain the 'Hardware'
    field value. Possible values:
        - Raspberry Pi 1 (model A, B, B+) and Zero is 2708
        - Raspberry Pi 2 (model B) is 2709
        - Raspberry Pi 3 (model B) on 4.9.x kernel is 2835
        - Anything else is not a Raspberry Pi"""

    try:
        # Opens the file and searches the field
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read()
    except IOError:
        print(Fore.RED + "No such file or directory: '/proc/cpuinfo'. This script must be run on a Raspberry Pi." + Fore.RESET)
        sys.exit(1)

    # Matches a line like 'Hardware   : BCMXXXX'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo, flags=re.MULTILINE | re.IGNORECASE)

    # 1. Couldn't find the 'Hardware' field. Assume that it isn't a Raspberry Pi
    # 2. Find the 'Hardware' field but the value is another one
    if not match or match.group(1) not in ('BCM2708', 'BCM2709', 'BCM2835'):
        print(Fore.RED + "You need to run this script on a Raspberry Pi." + Fore.RESET)
        sys.exit(1)


def check_concurrency():
    """Checks whether this script is or not already running"""

    filename = "raspberrypi_hyot.py"        # Name of the file
    count = 0                               # Process number counter

    # Obtains all pids
    for pid in psutil.pids():
        p = psutil.Process(pid)

        if p.name() == "python" and len(p.cmdline()) > 1 and filename in p.cmdline()[1]:
            # Another instance is running
            if count >= 1:
                print(Fore.RED + "Process: %s is already running with PID %s." % (filename, p.pid) + Fore.RESET)
                sys.exit(1)
            else:
                count += 1


def main():
    """Main function"""

    # Try-Catch block
    try:

        # Variables
        global uuid_dht11
        count = 0  # Measurement counter
        uuid_dht11 = None  # UUID of each DHT11 sensor measurement

        # Header
        print(Fore.BLUE + FIGLET.renderText("HYOT") + Fore.RESET)
        print(
            Style.BRIGHT + Fore.BLACK + "This script monitors several events -distance, temperature and humidity- from "
                                        "sensors, outputs by console and sends them to the cloud.\n"
            + Style.RESET_ALL + Fore.RESET)         # TODO

        time.sleep(2)                               # Wait time - 2 seconds

        # Initializing
        LCD.backlight_enabled = True                # Enables the backlight
        time.sleep(1)
        print("-> Initializing Raspberry Pi...")
        LCD.write_string("Initializing")            # Writes the specified unicode string to the display
        LCD.crlf()                                  # Writes a line feed and a carriage return (\r\n) character
        LCD.write_string("Raspberry Pi...")
        time.sleep(3)
        LCD.clear()                                 # Overwrites display with blank characters and reset cursor position
        time.sleep(1)

        # Reading values
        print("-> Reading values each 3 seconds from sensors\n")
        LCD.write_string("Reading values")
        LCD.crlf()
        LCD.write_string("from sensors")
        time.sleep(2)
        LCD.clear()
        time.sleep(1)

        # DHT11 sensor TODO
        LCD.write_string("- DHT11 sensor -")
        time.sleep(2)
        LCD.clear()

        # Loop each 3 seconds, hence, this is the time between measurements
        while True:

            # Increment the counter
            count += 1

            # ############### DHT11 SENSOR ###############

            # Obtains humidity and temperature
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PINDATA)
            # Obtains the datetime
            measure_datetime = datetime.datetime.now()

            print(Style.BRIGHT + Fore.CYAN + "DHT11 sensor - Measurement %i" % count + Style.RESET_ALL + Fore.RESET)

            # Checks the values
            if humidity is not None and 0 <= humidity <= 100 and temperature is not None and temperature >= 0:

                # Generates a random UUID
                uuid_dht11 = uuid.uuid4()

                # Outputs the data by console
                print(Style.BRIGHT + "UUID: " + Style.RESET_ALL + str(uuid_dht11))
                print("Datetime: " + str(measure_datetime.strftime("%d-%m-%Y %H:%M:%S %p")))
                print("Temperature: {0:0.1f} °C \nHumidity: {1:0.1f} %".format(temperature, humidity))

                # Outputs the data by display
                LCD.cursor_pos = (0, 0)
                LCD.write_string("Temp: %.1f °C" % temperature)
                LCD.crlf()
                LCD.write_string("Humidity: %.1f %%" % humidity)

            elif humidity is None or 0 > humidity > 100:                        # Humidity value is invalid or None
                print("Failed to get reading. Humidity is invalid or None")

            elif temperature is None or temperature < 0:                        # Temperature value is invalid or None
                print("Failed to get reading. Temperature is invalid or None")

            print("-----------------------------")

            time.sleep(3)

    except Exception as error:                          # TODO - Too general exception
        print(Fore.RED + "Error: " + str(error) + Fore.RESET + "\r")
    except KeyboardInterrupt:
        print("\r")  # TODO
        print(Fore.RED + "Exception: KeyboardInterrupt. Please, turn off the system for proper operation." + Fore.RESET)
    finally:
        LCD.close(clear=True)                           # Closes and calls the clear function
        LCD.backlight_enabled = False                   # Disables the backlight


########################################
#             MAIN PROGRAM             #
########################################
if __name__ == '__main__':

    check_root()                # Function to check the user
    check_platform()            # Checks whether the script is run on GNU/Linux platform
    check_raspberrypi()         # Checks whether the script is run on a Raspberry Pi
    check_concurrency()         # Checks whether the script is or not already running
    constants()                 # Declares all the constants
    main()                      # Main function
