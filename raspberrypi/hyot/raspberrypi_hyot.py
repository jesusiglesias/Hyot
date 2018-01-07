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
#   REQUIREMENTS:     Root user, Connected devices: LCD 16x2 (2), DTH11 sensor and HC-SR04 sensor,                     #
#                     Modules: checks_module.py                                                                        #
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
    import traceback                                # Print or retrieve a stack traceback
    import uuid                                     # UUID objects according to RFC 4122
    import time                                     # Time access and conversions
    import datetime                                 # Basic date and time types
    import checks_module as checks                  # Module to execute initial checks and to parse the menu
    import cloudantdb_module as cloudantdb          # Module that contains the logic of the Cloudant NoSQL DB service
    from pyfiglet import Figlet                     # Text banners in a variety of typefaces
    from colorama import Fore, Style                # Cross-platform colored terminal text
    import Adafruit_DHT                             # DHT11 sensor
    from RPLCD.i2c import CharLCD                   # LCD 16x2

except ImportError as importError:
    print("Error to import: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
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
        print(Fore.RED + "IOError in constants() function: " + str(ioError) + ". Main errno:" + "\r")
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
        print("\r" + Fore.RED + "Exception: KeyboardInterrupt. Please, do not interrupt the execution." + Fore.RESET)
        sys.exit(1)


########################################
#               FUNCTIONS              #
########################################
def header():
    """Prints the header in the console"""

    # Header
    print(Fore.BLUE + FIGLET.renderText("HYOT") + Fore.RESET)
    print(
            Style.BRIGHT + Fore.BLACK + "This script monitors several events -distance, temperature and humidity- from "
                                        "sensors, outputs by console and sends them to the cloud.\n"
            + Style.RESET_ALL)                      # TODO

    time.sleep(1)                                   # Wait time - 1 second


def timestamp():
    """Generates a timestamp string for each measurement and for each image/video taken"""  # TODO

    return datetime.datetime.now()


def main():
    """Main function"""

    # Try-Catch block
    try:

        # Variables
        global dht11_uuid
        count = 0                                   # Measurement counter
        dht11_uuid = None                           # UUID of each DHT11 sensor measurement

        # Header
        header()

        # Initializing
        LCD.backlight_enabled = True                # Enables the backlight
        time.sleep(1)
        print("-> Initializing Raspberry Pi...")
        LCD.write_string("Initializing")            # Writes the specified unicode string to the display
        LCD.crlf()                                  # Writes a line feed and a carriage return (\r\n) character
        LCD.write_string("Raspberry Pi...")
        time.sleep(3)
        # ############### Initializing databases ###############
        cloudantdb.connect()                        # Creates a Cloudant DB client and establishes a connection
        cloudantdb.init(timestamp())                # Initializes the databases
        time.sleep(2)
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

                # Create a JSON document content data
                dht11_data = {
                    '_id': str(dht11_uuid),
                    "datetime_field": str(measure_datetime.strftime("%d-%m-%Y %H:%M:%S %p")),
                    "temperature_field": temperature,
                    "humidity_field": humidity,
                }

                # Adds the document to the database of the Cloudant NoSQL service
                cloudantdb.add_document(dht11_data, cloudantdb.SENSORS[0])

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

    except IOError as ioError:                      # Related to LCD 16x2 and Cloudant NoSQL DB
        print(Fore.RED + "\nIOError in the main() function or in the modules: " + str(ioError) + ". Main reasons:")
        print("\n- Cloudant NoSQL DB service")
        print("      401 Unauthorized: credentials do not have permission to access to the specified Cloudant instance."
              "\r")
        print("      Errno -2: cloudant instance (URL) is wrong or unknown.\r")
        print("- LCD - I2C protocol")
        print("      Errno 2: I2C interface is disabled.\r")
        print("      Errno 22: I2C address is invalid.\r")
        print("      Errno 121: LCD is not connected.\r")
        sys.exit(1)
    except Exception as exception:                  # TODO - Too general exception
        print(Fore.RED + "\nException in the main() function or in the modules: " + str(exception.message.lower()) +
              ".")
        traceback.print_exc()                       # Prints the traceback
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:                       # TODO
        print("\r" + Fore.RED + "Exception: KeyboardInterrupt. Please, turn off the system for proper operation."
              + Fore.RESET)
        sys.exit(1)
    finally:
        LCD.close(clear=True)                       # Closes and calls the clear function
        LCD.backlight_enabled = False               # Disables the backlight
        try:
            LCD.close(clear=True)                   # Closes and calls the clear function
            LCD.backlight_enabled = False           # Disables the backlight
            cloudantdb.disconnect()                 # Disconnects the Cloudant client
        except Exception as finallyException:       # TODO - Too general exception
            print(Fore.RED + "\nException in the finally statement of the main() function: " +
                  str(finallyException.message.lower()) + ".")
            traceback.print_exc()                   # Prints the traceback
            print(Fore.RESET)
            sys.exit(1)


########################################
#             MAIN PROGRAM             #
########################################
if __name__ == '__main__':

    checks.check_root()                # Function to check the user
    checks.check_platform()            # Checks if the script is run on GNU/Linux platform
    checks.check_raspberrypi()         # Checks if the script is run on a Raspberry Pi
    checks.check_network()             # Checks if the Raspberry Pi is connected to the network
    checks.check_concurrency()         # Checks if the script is or not already running
    arguments = checks.menu()          # Checks the options entered by the user when running the script
    constants(arguments)               # Declares all the constants
    main()                             # Main function
