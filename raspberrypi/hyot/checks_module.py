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
#           FILE:     checks_module.py                                                                                 #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module executes several initial checks and parses the menu                                  #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/05/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module executes several initial checks and parses the menu"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import os                                       # Miscellaneous operating system interfaces
    import re                                       # Regular expression
    import traceback                                # Print or retrieve a stack traceback
    import socket                                   # Low-level networking interface
    import argparse                                 # Python command-line parsing library
    import psutil                                   # Python system and process utilities
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in checks_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#               FUNCTIONS              #
########################################
def check_root():
    """Checks that the script is run as a root user"""

    if not os.geteuid() == 0:
        print(Fore.RED + "You need to have root privileges to run this script. Please try it again using "
                         "'sudo'." + Fore.RESET)
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
        print(Fore.RED + "No such file or directory: '/proc/cpuinfo'. This script must be run on a Raspberry "
                         "Pi." + Fore.RESET)
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
        print(Fore.RED + "Raspberry Pi is not connected to the network. Please, enable the network to continue "
                         "the execution." + Fore.RESET)
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


def __is_valid_email(email):
    """Checks if the email is valid
    :param email: Email entered
    :return: True/False based on the validity of the email
    """

    if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', str(email)) is not None:
        return True
    else:
        return False


def menu():
    """Checks the options entered by the user when running the script
    :return: args Values of the arguments entered by the user in the console
    """

    try:

        # Creates a parser TODO - Description
        parser = argparse.ArgumentParser(
            description=Style.BRIGHT + "HYOT/HELP:" + Style.RESET_ALL + " This script monitors several events "
                                       "-distance, temperature and humidity- from sensors, outputs by console and "
                                       "sends them to the cloud." + Fore.RED + " Remember " + Fore.RESET + "to run "
                                       "this script with root user or sudo and the options are optional. If not given,"
                                       " default values are used.",
            add_help=False)

        # Groups TODO - Name
        general_group = parser.add_argument_group('General options')
        pin_group = parser.add_argument_group('Sensor and device pin')
        i2c_group = parser.add_argument_group('LCD device - I2C')
        threshold_group = parser.add_argument_group('Alert threshold')

        # ### General group ###
        # Help option
        general_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                                   help='Shows the help.')

        # Email address where to send an alert notification
        general_group.add_argument("-e", "--email",
                                   default=None, required=False, action="store", dest="EMAIL",
                                   help="Email address where to send an alert notification. Default: disabled option.")

        # Time that the recording will take when an alert is triggered
        general_group.add_argument("-r", "--recordingtime",
                                   type=int, default=10, required=False, action="store", dest="RECORDING_TIME",
                                   help="Time that the recording will take when an alert is triggered (e.g. 10 seconds)"
                                        ". Default: 10.")

        # Wait time between measurements TODO - Group
        general_group.add_argument("-wt", "--waittime",
                                   type=int, default=3, required=False, action="store", dest="WAITTIME_MEASUREMENTS",
                                   help="Wait time between measurements in the sensors (e.g. 3 seconds). Default: 3.")

        # ### Pin group ###
        # DHT11 sensor - Data pin
        pin_group.add_argument("-dd", "--dht11data",
                               type=int, default=21, required=False, action="store", dest="DHT_DATAPIN",
                               help="Data pin for DHT11 sensor in Broadcom GPIO pin number (e.g. 21 for Raspberry Pi "
                                    "GPIO21). Default: 21.")

        # Red led - Pin
        pin_group.add_argument("-lp", "--ledpin",
                               type=int, default=13, required=False, action="store", dest="LED_PIN",
                               help="Pin for LED in Broadcom GPIO pin number (e.g. 13 for Raspberry Pi "
                                    "GPIO13). Default: 13.")

        # ### I2C group ###
        # LCD 16x2 - DHT11 I2C Expander
        i2c_group.add_argument("-die", "--dhti2cexpander",
                               default="PCF8574", required=False, action="store", dest="DHT_I2CEXPANDER",
                               help="I2C expander type for LCD 16x2 of the DH11 sensor. One of 'PCF8574', 'MCP23008', "
                                    "'MCP23017'. Default: PCF8574.")

        # LCD 16x2 - DHT11 I2C address
        i2c_group.add_argument("-dia", "--dhti2caddress",
                               default="0x3f", required=False, action="store", dest="DHT_I2CADDRESS",
                               help="I2C address for LCD 16x2 of the DH11 sensor. Type the 'i2cdetect -y 1' (RPi v.3) "
                                    "command to obtain it. Default: 0x3f.")

        # LCD 16x2 - HC-SR04 I2C Expander
        i2c_group.add_argument("-hie", "--hcsri2cexpander",
                               default="PCF8574", required=False, action="store", dest="HCSR_I2CEXPANDER",
                               help="I2C expander type for LCD 16x2 of the HC-SR04 sensor. One of 'PCF8574', "
                                    "'MCP23008', 'MCP23017'. Default: PCF8574.")

        # LCD 16x2 - HC-SR04 I2C address
        i2c_group.add_argument("-hia", "--hcsri2caddress",
                               default="0x38", required=False, action="store", dest="HCSR_I2CADDRESS",
                               help="I2C address for LCD 16x2 of the HC-SR04 sensor. Type the 'i2cdetect -y 1' "
                                    "(RPi v.3) command to obtain it. Default: 0x38.")

        # ### Threshold group ###
        # DHT11 sensor - Temperature threshold TODO
        threshold_group.add_argument("-tt", "--tempthreshold",
                                     type=int, default=30, required=False, action="store", dest="TEMPERATURE_THRESHOLD",
                                     help="Temperature alert threshold in the DHT11 sensor (e.g. 30 °C). Default: 30.")

        # DHT11 sensor - Humidity threshold TODO
        threshold_group.add_argument("-ht", "--humthreshold",
                                     type=int, default=80, required=False, action="store", dest="HUMIDITY_THRESHOLD",
                                     help="Humidity alert threshold in the DHT11 sensor (e.g. 80 %%). Default: 80.")

        # Parses the arguments returning the data from the options specified
        args = parser.parse_args()

        # Checks the '--email' argument
        if args.EMAIL:
            if not __is_valid_email(args.EMAIL):
                print(Fore.RED + "Email address entered is not a valid email. Please, type the '-h/--help' option to "
                                 "show the help." + Fore.RESET)
                sys.exit(1)

        # Checks the '--recordingtime' argument
        if args.RECORDING_TIME < 1:
            print(Fore.RED + "Recording time invalid. Please, type the '-h/--help' option to show the help"
                             " or the value must be upper than 0. Default value: 10." + Fore.RESET)
            sys.exit(1)

        # Checks the '--waittime' argument
        if args.WAITTIME_MEASUREMENTS < 2:
            print(Fore.RED + "Wait time between measurements invalid. Please, type the '-h/--help' option to show the "
                             "help or a value in seconds upper than 2. Default value: 3." + Fore.RESET)
            sys.exit(1)

        # Checks the '--dht11data' argument
        if args.DHT_DATAPIN < 0 or args.DHT_DATAPIN > 27:
            print(Fore.RED + "Data pin for DHT11 sensor invalid. Please, type the '-h/--help' option to show the help"
                             " or the number in Broadcom GPIO format and in the range 0-27. Default value: 21."
                  + Fore.RESET)
            sys.exit(1)

        # Checks the '--ledpin' argument
        if args.LED_PIN < 0 or args.LED_PIN > 27:
            print(Fore.RED + "Pin for led invalid. Please, type the '-h/--help' option to show the help"
                             " or the number in Broadcom GPIO format and in the range 0-27. Default value: 13."
                  + Fore.RESET)
            sys.exit(1)

        # Checks the '--dhti2cexpander' argument
        if args.DHT_I2CEXPANDER not in ['PCF8574', 'MCP23008', 'MCP23017']:
            print(Fore.RED + "I2C expander type for LCD of the DHT11 sensor invalid. Please, type the '-h/--help' "
                             "option to show the help or specify one of 'PCF8574', 'MCP23008', 'MCP23017'. "
                             "Default value: PCF8574." + Fore.RESET)
            sys.exit(1)

        # Checks the '--hcsri2cexpander' argument
        if args.HCSR_I2CEXPANDER not in ['PCF8574', 'MCP23008', 'MCP23017']:
            print(Fore.RED + "I2C expander type invalid for LCD of the HC-SR04 sensor invalid. Please, type the "
                             "'-h/--help' option to show the help or specify one of 'PCF8574', 'MCP23008', 'MCP23017'."
                             " Default value: PCF8574." + Fore.RESET)
            sys.exit(1)

        # Checks the '--tempthreshold' argument
        if args.TEMPERATURE_THRESHOLD < 0:
            print(Fore.RED + "Temperature alert threshold invalid. Please, type the '-h/--help' option to show the help"
                             " or the value must be upper than 0. Default value: 30." + Fore.RESET)
            sys.exit(1)

        # Checks the '--humthreshold' argument
        if args.HUMIDITY_THRESHOLD < 0 or args.HUMIDITY_THRESHOLD > 100:
            print(Fore.RED + "Humidity alert threshold invalid. Please, type the '-h/--help' option to show the help"
                             " or the value must be the 0-100 range. Default value: 80." + Fore.RESET)
            sys.exit(1)

        return args

    except Exception as argparseError:
        print(Fore.RED + "\nException in the menu() function: " + str(argparseError.message.lower()) + ".")
        traceback.print_exc()       # Prints the traceback
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\r" + Fore.RED + "Exception: KeyboardInterrupt. Please, do not interrupt the execution." + Fore.RESET)
        sys.exit(1)
