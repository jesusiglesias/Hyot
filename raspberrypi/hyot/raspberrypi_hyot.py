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
#   REQUIREMENTS:     Root user, Connected devices: LCD 16x2 (2), Picamera, DTH11 sensor and HC-SR04 sensor,           #
#                     Modules: camera_module.py, checks_module.py, cloudantdb_module.py, dropbox_module.py,            #
#                     email_module.py, lcd_module.py, system_module.py                                                 #
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
from __future__ import unicode_literals             # Future statement definitions TODO Delete

try:
    import sys                                      # System-specific parameters and functions
    import traceback                                # Print or retrieve a stack traceback
    import uuid                                     # UUID objects according to RFC 4122
    import time                                     # Time access and conversions
    import datetime                                 # Basic date and time types
    import camera_module as picamera                # Module to handle the Picamera
    import checks_module as checks                  # Module to execute initial checks and to parse the menu
    import cloudantdb_module as cloudantdb          # Module that contains the logic of the Cloudant NoSQL DB service
    import dropbox_module as dropbox                # Module that contains the logic of the Dropbox service
    import email_module as email                    # Module to send emails when an alert is triggered
    import lcd_module as lcd                        # Module to handle the LCDs
    import system_module as system                  # Module that performs functions in the local operating system
    from pyfiglet import Figlet                     # Text banners in a variety of typefaces
    from colorama import Fore, Style                # Cross-platform colored terminal text
    from gpiozero import LED                        # Simple interface to GPIO devices
    import Adafruit_DHT                             # DHT11 sensor

except ImportError as importError:
    print("Error to import in raspberrypi_hyot: " + importError.message.lower() + ".")
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

    global FIGLET, SENSORS, DHT11_EVENTS, MAILTO, TIME_MEASUREMENTS, DHT_SENSOR, DHT_PINDATA, TEMP_THRESHOLD, \
        HUM_THRESHOLD, ALERT_LED

    try:

        FIGLET = Figlet(font='future_8', justify='center')          # Figlet
        SENSORS = ["DHT11", "HC-SR04"]                              # Name of the sensors
        DHT11_EVENTS = ["Temperature", "Humidity"]                  # Name of the events of the DHT11 sensor
        MAILTO = user_args.EMAIL                                    # Recipient's email address
        TIME_MEASUREMENTS = user_args.WAITTIME_MEASUREMENTS         # Wait time between each measurement. Default 3 seconds
        DHT_SENSOR = Adafruit_DHT.DHT11                             # DHT11 sensor
        DHT_PINDATA = user_args.DHT_DATAPIN                         # DHT11 - Data pin. Default 21 (GPIO21)
        TEMP_THRESHOLD = user_args.TEMPERATURE_THRESHOLD            # Temperature alert threshold in the DHT11 sensor
        HUM_THRESHOLD = user_args.HUMIDITY_THRESHOLD                # Humidity alert threshold in the DHT11 sensor
        ALERT_LED = LED(user_args.LED_PIN)                          # Led pin. Default 13 (GPIO13)

    except Exception as exception:                  # TODO - Too general exception
        print(Fore.RED + "Exception in constants() function: " + str(exception))
        traceback.print_exc()                       # Prints the traceback
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\r" + Fore.RED + "Exception: KeyboardInterrupt. Please, do not interrupt the execution." + Fore.RESET)
        sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
uuid_measurement = None                     # UUID of each measurement for both sensors
datetime_measurement = None                 # Datetime in which the measurement was taken
video_filename = None                       # Name of the video file
video_filefullpath = None                   # Full path of the recording
ext = '.h264'                               # Extension of the video file
recording_time = None                       # Time that the recording will take
alert_triggered = None                      # Indicates if an alert has been triggered
alert_origin = None                         # Indicates which event triggered the alert
threshold_value = None                      # Indicates the value of the event threshold that triggers the alert
link_dropbox = None                         # Shared link of the uploaded file to Dropbox
sent = None                                 # Indicates if the email was or not sent


########################################
#               FUNCTIONS              #
########################################
def header():
    """Prints the header in the console"""

    global FIGLET

    # Header
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + FIGLET.renderText("HYOT"))
    print("This script monitors several events -distance, temperature and humidity- from sensors, outputs by console "
          "and sends them to the cloud.\n" + Style.RESET_ALL)                      # TODO

    time.sleep(1)                                   # Wait time - 1 second


def timestamp():
    """Generates a timestamp string for each measurement and for each image/video taken"""  # TODO

    return datetime.datetime.now()


def information_values():
    """Shows the information by console about some values established"""

    global TEMP_THRESHOLD, HUM_THRESHOLD, TIME_MEASUREMENTS, recording_time

    print(Style.BRIGHT + Fore.BLACK + "\n-- Information - Values established:" + Style.RESET_ALL)
    # Information about the current thresholds
    print(Fore.BLACK + "      -- Alert thresholds:")
    print("        - Sensor: DHT11 - Event: Temperature -> " + str(TEMP_THRESHOLD) + ' °C')
    print("        - Sensor: DHT11 - Event: Humidity -> " + str(HUM_THRESHOLD) + ' %')
    print("        - Sensor: HC-SR04 - Event: Distance -> " + ' meters')  # TODO
    # Information about the recording time
    print(Fore.BLACK + "      -- Recording time: " + str(recording_time) + " seconds")
    # Information about the time between measurements
    print(Fore.BLACK + "      -- Time between measurements: " + str(TIME_MEASUREMENTS) + " seconds")

    time.sleep(2)


def reset_values():
    """Resets the values"""

    global video_filename, video_filefullpath, alert_triggered, alert_origin, threshold_value, link_dropbox, sent

    video_filename = None
    video_filefullpath = None
    alert_triggered = False
    alert_origin = None
    threshold_value = None
    link_dropbox = None
    sent = None


def add_cloudant(sensor, temperature, humidity):
    """Adds the data to the Cloudant NoSQL database
    :param sensor: Indicates the sensor that triggered the alert
    :param temperature: Indicates the value of temperature measured
    :param humidity: Indicates the value of humidity measured
    """

    global uuid_measurement, datetime_measurement, alert_triggered, alert_origin, threshold_value, link_dropbox, sent,\
        MAILTO

    # Creates a JSON document content data
    data = {
        '_id': str(uuid_measurement),
        "datetime_field": str(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p")),
        "temperature_field": temperature,
        "humidity_field": humidity,
        "alert_triggered": alert_triggered,
        "alert_origin": alert_origin,
        "threshold_value": threshold_value,
        "shared_link_Dropbox": link_dropbox,
        "notification_sent": sent,
        "mailto": MAILTO
    }

    # Adds the document to the database of the Cloudant NoSQL service
    cloudantdb.add_document(data, sensor)


def alert_procedure(sensor, event, temperature, humidity):
    """Initiates the alert procedure
    :param sensor: Indicates the sensor that triggered the alert
    :param event: Indicates the event that triggered the alert
    :param temperature: Indicates the value of temperature measured
    :param humidity: Indicates the value of humidity measured
    """

    global uuid_measurement, datetime_measurement, video_filename, video_filefullpath, ext, recording_time, \
        alert_triggered, alert_origin, threshold_value, link_dropbox, sent, MAILTO, ALERT_LED

    # Name of the video file
    video_filename = sensor.lower() + '_' + event.lower() + '_' + str(datetime_measurement.strftime("%d%m%Y_%H%M%S")) + ext

    # Full path of the video file
    video_filefullpath = system.tempfiles_path + '/' + video_filename

    alert_triggered = True                                              # Marks the alert like triggered
    alert_origin = sensor + ' - ' + event                               # Saves the event which triggers the alert
    time.sleep(1)
    lcd.clear_lcd(sensor)                                               # Clears the LCD
    time.sleep(1)

    print(Fore.RED + "  ---------- ALERT TRIGGERED | " + sensor + " | " + event + " ----------  " + Fore.RESET)
    lcd.full_print_lcd(sensor, "ALERT TRIGGERED!", event)
    ALERT_LED.on()                                                      # Turns on the red led
    time.sleep(3)

    lcd.clear_lcd(sensor)                                               # Clears the LCD
    print(Fore.BLACK + "  ----------- Initiating the alert procedure ------------  " + Fore.RESET)
    lcd.full_print_lcd(sensor, "Initiating the", "procedure...")

    # Takes a recording for 10 seconds
    picamera.record_video(video_filefullpath, recording_time)

    # Checks if the file exists in the local system
    system.check_file(video_filefullpath)

    # Uploads the file to Dropbox
    link_dropbox = dropbox.upload_file(video_filefullpath, video_filename, sensor)

    # Sends an email when an alert is triggered
    if not (MAILTO is None):
        sent = email.send_email(MAILTO, video_filefullpath, video_filename,  # TODO - Distance
                                str(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p")),
                                str(uuid_measurement), temperature, humidity, "1", link_dropbox,
                                alert_origin, threshold_value)

    # Removes the temporary file after uploading to Dropbox
    system.remove_file(video_filefullpath)

    # Adds the measurement to the database
    add_cloudant(sensor, temperature, humidity)

    time.sleep(1)
    lcd.clear_lcd(sensor)                                       # Clears the LCD
    ALERT_LED.off()                                             # Turns off the red led
    time.sleep(1)
    print(Fore.RED + "  ----------- PROCEDURE FINISHED. CONTINUING... ----------  " + Fore.RESET)
    lcd.full_print_lcd(sensor, "Procedure", "finished...")


def main(user_args):
    """Main function
    :param user_args: Values of the options entered by the user
    """

    # Try-Catch block
    try:

        # Variables
        global uuid_measurement, datetime_measurement, recording_time, threshold_value, SENSORS, MAILTO, \
            TIME_MEASUREMENTS, DHT_SENSOR, DHT_PINDATA, DHT11_EVENTS, TEMP_THRESHOLD, HUM_THRESHOLD

        count = 0                                   # Measurement counter
        recording_time = user_args.RECORDING_TIME   # Time that the recording will take

        # Header
        header()

        # ############### Initializing HYOT ###############
        print(Style.BRIGHT + Fore.BLACK + "-- Initializing HYOT..." + Style.RESET_ALL)

        # ############### Initializing LCDs ###############
        lcd.init(user_args.DHT_I2CEXPANDER, user_args.DHT_I2CADDRESS, user_args.HCSR_I2CEXPANDER,
                 user_args.HCSR_I2CADDRESS, SENSORS)  # Initializes the LCD instances

        # ############### Initializing the Picamera ###############
        picamera.init()                             # Initializes the Picamera

        # ############### Initializing local directory ###############
        system.create_localdir()                    # Creates a local directory to store the files taken by the Picamera

        # ############### Initializing the mail session ###############
        if not (MAILTO is None):
            email.init()                            # Initializes the mail session

        # ############### Initializing databases ###############
        cloudantdb.connect()                        # Creates a Cloudant DB client and establishes a connection
        cloudantdb.init(timestamp(), SENSORS)       # Initializes the databases

        # ############### Initializing Dropbox ###############
        dropbox.connect()                           # Creates a Dropbox client and establishes a connection
        dropbox.init(SENSORS)                       # Initializes the main directory and the subdirectories

        time.sleep(2)                               # Wait time - 2 seconds
        lcd.clear_lcds()                            # Clears both LCDs
        time.sleep(1)                               # Wait time - 1 second

        # ############### Information - Values established ###############
        information_values()

        # ############### Reading values ###############
        print(Style.BRIGHT + Fore.BLACK + "\n-- Reading values each " + str(TIME_MEASUREMENTS) + " seconds from "
                                          "sensors\n" + Style.RESET_ALL)

        lcd.full_print_lcds("Reading values", "from sensors")           # Writes in both LCDS using both rows
        time.sleep(1)
        lcd.clear_lcds()
        time.sleep(1)

        # DHT11 and HC-SR04 sensor TODO
        lcd.print_lcds("- DHT11 sensor -", " HC-SR04 sensor ")
        time.sleep(2)
        lcd.clear_lcds()

        # Loop each n seconds, hence, this is the time between measurements
        while True:

            count += 1                                                  # Increment the counter
            datetime_measurement = timestamp()                          # Obtains a timestamp (datetime)
            uuid_measurement = uuid.uuid4()                             # Generates a random UUID
            reset_values()                                              # Resets the values

            # ############### DHT11 SENSOR ###############

            # Obtains humidity and temperature
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PINDATA)

            print(Style.BRIGHT + Fore.CYAN + "DHT11 sensor - Measurement %i" % count + Style.RESET_ALL)

            # Checks the values
            if humidity is not None and 0 <= humidity <= 100 and temperature is not None and temperature >= 0:

                # Outputs the data by console
                print(Style.BRIGHT + "UUID: " + Style.RESET_ALL + Fore.BLACK + str(uuid_measurement))
                print("Datetime: " + str(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p")))
                print("Temperature: {0:0.1f} °C \nHumidity: {1:0.1f} %".format(temperature, humidity) + Fore.RESET)

                # Outputs the data by LCD
                lcd.print_measure_dht(temperature, humidity, False, False)

                # Alert - DHT11 | Temperature TODO - Pass events - Distance
                if temperature > TEMP_THRESHOLD:
                    threshold_value = TEMP_THRESHOLD
                    alert_procedure(SENSORS[0], DHT11_EVENTS[0], temperature, humidity)

                # Alert - DHT11 | Humidity
                elif humidity > HUM_THRESHOLD:
                    threshold_value = HUM_THRESHOLD
                    alert_procedure(SENSORS[0], DHT11_EVENTS[1], temperature, humidity)

                # No alert
                else:
                    add_cloudant(SENSORS[0], temperature, humidity)

            elif humidity is None or 0 > humidity > 100:                        # Humidity value is invalid or None
                print("Failed to get reading. Humidity is invalid or None")

                # Shows the output like empty
                lcd.print_measure_dht(None, None, True, True)

            elif temperature is None or temperature < 0:                        # Temperature value is invalid or None
                print("Failed to get reading. Temperature is invalid or None")

                # Shows the output like empty
                lcd.print_measure_dht(None, None, True, True)

            print("-----------------------------")

            time.sleep(TIME_MEASUREMENTS - 1)

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
        print(Style.BRIGHT + Fore.BLACK + "\n-- Ending HYOT..." + Style.RESET_ALL)
        try:
            print("\r")
            lcd.disconnect_lcds()                       # Disconnects the LCDs
            picamera.disconnect()                       # Disconnects the Picamera
            system.remove_localdir()                    # Removes the temporary local directory
            email.disconnect()                          # Disconnects the mail session
            cloudantdb.disconnect()                     # Disconnects the Cloudant client
            dropbox.disconnect()                        # Disables the access token used to authenticate the calls
            print("\r")
        except Exception as finallyException:           # TODO - Too general exception
            print(Fore.RED + "\nException in the finally statement of the main() function: " +
                  str(finallyException.message.lower()) + ".")
            traceback.print_exc()                       # Prints the traceback
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
    main(arguments)                    # Main function
