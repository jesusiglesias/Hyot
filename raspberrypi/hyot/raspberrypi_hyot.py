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
#          USAGE:     sudo python raspberrypi_hyot.py                                                                  #
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
    import traceback                                # Print or retrieve a stack traceback
    import uuid                                     # UUID objects according to RFC 4122
    import socket                                   # Low-level networking interface
    import argparse                                 # Python command-line parsing library
    import time                                     # Time access and conversions
    import datetime                                 # Basic date and time types
    import psutil                                   # Python system and process utilities
    from pyfiglet import Figlet                     # Text banners in a variety of typefaces
    from colorama import Fore, Style                # Cross-platform colored terminal text
    import Adafruit_DHT                             # DHT11 sensor
    from RPLCD.i2c import CharLCD                   # LCD 16x2

except ImportError as importError:
    print("Error to import: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
def constants(user_args):
    """Contains all definitions of constants
    :param user_args: Values of the options entered by the user
    """

    global FIGLET, TIME_MEASUREMENTS, DHT_SENSOR, DHT_PINDATA, LCD

    try:

        FIGLET = Figlet(font='future_8', justify='center')      # Figlet
        TIME_MEASUREMENTS = user_args.WAITTIME_MEASUREMENTS     # Wait time between each measurement. Default 3 seconds
        DHT_SENSOR = Adafruit_DHT.DHT11                         # DHT11 sensor
        DHT_PINDATA = user_args.DHT_DATAPIN                     # DHT11 - Data pin. Default 21 (GPIO21)
        LCD = CharLCD(i2c_expander=user_args.I2C_EXPANDER,      # LCD 16x2. Default 'PCF8574' and 0x3f
                      address=int(user_args.I2C_ADDRESS, base=16),
                      charmap='A00',
                      backlight_enabled=False)

    except IOError as ioError:                      # Related to LCD 16x2
        print(Fore.RED + "IOError in constants() function: " + str(ioError) + "." + "\r")
        print("- Errno 2: I2C interface is disabled.\r")
        print("- Errno 22: I2C address is invalid.\r")
        print("- Errno 121: LCD is not connected.\r")
        sys.exit(1)
    except Exception as exception:                  # TODO - Too general exception
        print(Fore.RED + "Exception in constants() function: " + str(exception))
        traceback.print_exc()                       # Prints the traceback
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Exception: KeyboardInterrupt. Please, do not interrupt the execution." + Fore.RESET)
        sys.exit(1)


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


def check_network():
    """Checks if the Raspberry Pi is connected to the network"""

    # Host: 8.8.8.8 (google-public-dns-a.google.com)
    # OpenPort: 53/tcp
    # Service: domain (DNS/TCP)

    # Variables
    host = "8.8.8.8"
    port = 53
    timeout = 5

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    except socket.error:
        print(Fore.RED + "Raspberry Pi is not connected to the network. Please, enable the network to continue the execution." + Fore.RESET)
        sys.exit(1)


def check_concurrency():
    """Checks if this script is or not already running"""

    # Variables
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


def menu():
    """Checks the options entered by the user when running the script
    :return: Values of the arguments entered by the user in the console
    """

    try:

        # Creates a parser TODO - Description
        parser = argparse.ArgumentParser(
            description=Style.BRIGHT + "HYOT/HELP:" + Style.RESET_ALL + " This script monitors several events -distance, "
                                       "temperature and humidity- from sensors, outputs by console and sends them to the "
                                       "cloud." + Fore.RED + " Remember " + Fore.RESET + "to run this script with root "
                                       "user or sudo and the options are optional. If not given, default values are used.",
            add_help=False)

        # Groups TODO - Name
        general_group = parser.add_argument_group('General options')
        pin_group = parser.add_argument_group('Sensor and device pin')
        i2c_group = parser.add_argument_group('LCD device - I2C')

        # Help option
        general_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                                   help='Shows the help.')

        # Wait time between measurements TODO - Group
        general_group.add_argument("-wt", "--waittime",
                                   type=int, default=3, required=False, action="store", dest="WAITTIME_MEASUREMENTS",
                                   help="Wait time between measurements in the sensors (e.g. 3 seconds). Default: 3.")

        # DHT11 sensor - Data pin
        pin_group.add_argument("-dd", "--dht11data",
                               type=int, default=21, required=False, action="store", dest="DHT_DATAPIN",
                               help="Data pin for DHT11 sensor in Broadcom GPIO pin number (e.g. 21 for Raspberry Pi "
                                    "GPIO21). Default: 21.")

        # LCD 16x2 - I2C Expander
        i2c_group.add_argument("-ie", "--i2cexpander",
                               default="PCF8574", required=False, action="store", dest="I2C_EXPANDER",
                               help="I2C expander type for LCD 16x2. One of 'PCF8574', 'MCP23008', 'MCP23017'. "
                                    "Default: PCF8574.")

        # LCD 16x2 - I2C address
        i2c_group.add_argument("-ia", "--i2caddress",
                               default="0x3f", required=False, action="store", dest="I2C_ADDRESS",
                               help="I2C address for LCD 16x2. Type the 'i2cdetect -y 1' (RPi v.3) command to obtain it. "
                                    "Default: 0x3f.")

        # Parses the arguments returning the data from the options specified
        args = parser.parse_args()

        # Checks the '--waittime' argument
        if args.WAITTIME_MEASUREMENTS < 1:
            print(Fore.RED + "Wait time between measurements invalid. Please, type the '-h/--help' option to show the help "
                             "or a value in seconds upper than 1. Default value: 3." + Fore.RESET)
            sys.exit(1)

        # Checks the '--dht11data' argument
        if args.DHT_DATAPIN < 0 or args.DHT_DATAPIN > 27:
            print(Fore.RED + "Data pin for DHT11 sensor invalid. Please, type the '-h/--help' option to show the help or "
                             "the number in Broadcom GPIO format and in the range 0-27. Default value: 21." + Fore.RESET)
            sys.exit(1)

        # Checks the '--i2cexpander' argument
        if args.I2C_EXPANDER not in ['PCF8574', 'MCP23008', 'MCP23017']:
            print(Fore.RED + "I2C expander type invalid. Please, type the '-h/--help' option to show the help or "
                             "specify one of 'PCF8574', 'MCP23008', 'MCP23017'. Default value: PCF8574.")
            sys.exit(1)

        return args

    except Exception as argparseError:
        print(Fore.RED + "\nException in menu() function: " + str(argparseError.message.lower()) + ".")
        traceback.print_exc()  # Prints the traceback
        print(Fore.RESET)


def timestamp():
    """Generates a timestamp string for each measurement and for each image/video taken"""  # TODO

    return datetime.datetime.now()


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
        print("-> Reading values each " + str(TIME_MEASUREMENTS) + " seconds from sensors\n")
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

        # Loop each n seconds, hence, this is the time between measurements
        while True:

            # Increment the counter
            count += 1

            # ############### DHT11 SENSOR ###############

            # Obtains humidity and temperature
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PINDATA)

            # Obtains a timestamp (datetime)
            measure_datetime = timestamp()

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

                # Shows the output like empty
                LCD.clear()
                LCD.cursor_pos = (0, 0)
                LCD.write_string("Temp: ")
                LCD.crlf()
                LCD.write_string("Humidity: ")

            elif temperature is None or temperature < 0:                        # Temperature value is invalid or None
                print("Failed to get reading. Temperature is invalid or None")

                # Shows the output like empty
                LCD.clear()
                LCD.cursor_pos = (0, 0)
                LCD.write_string("Temp: ")
                LCD.crlf()
                LCD.write_string("Humidity: ")

            print("-----------------------------")

            time.sleep(TIME_MEASUREMENTS)

    except IOError as ioError:                      # Related to LCD 16x2
        print(Fore.RED + "\nIOError in main() function: " + str(ioError) + ". Main errno:" + "\r")
        print("- Errno 2: I2C interface is disabled.\r")
        print("- Errno 22: I2C address is invalid.\r")
        print("- Errno 121: LCD is not connected.\r")
    except Exception as exception:                  # TODO - Too general exception
        print(Fore.RED + "\nException in main() function: " + str(exception.message.lower()) + ".")
        traceback.print_exc()                       # Prints the traceback
        print(Fore.RESET)
    except KeyboardInterrupt:
        print("\r")                                 # TODO
        print(Fore.RED + "Exception: KeyboardInterrupt. Please, turn off the system for proper operation." + Fore.RESET)
    finally:
        LCD.close(clear=True)                       # Closes and calls the clear function
        LCD.backlight_enabled = False               # Disables the backlight


########################################
#             MAIN PROGRAM             #
########################################
if __name__ == '__main__':

    check_root()                # Function to check the user
    check_platform()            # Checks if the script is run on GNU/Linux platform
    check_raspberrypi()         # Checks if the script is run on a Raspberry Pi
    check_network()             # Checks if the Raspberry Pi is connected to the network
    check_concurrency()         # Checks if the script is or not already running
    arguments = menu()          # Checks the options entered by the user when running the script
    constants(arguments)        # Declares all the constants
    main()                      # Main function
