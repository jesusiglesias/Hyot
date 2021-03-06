#!/usr/bin/python
# -*- coding: utf-8 -*-
# =====================================================================================================================#
#                                                                                                                      #
#                                              _    ___     ______ _______                                             #
#                                             | |  | \ \   / / __ \__   __|                                            #
#                                             | |__| |\ \_/ / |  | | | |                                               #
#                                             |  __  | \   /| |  | | | |                                               #
#                                             | |  | |  | | | |__| | | |                                               #
#                                             |_|  |_|  |_|  \____/  |_|                                               #
#                                                                                                                      #
#                    _____                         _     _ _ _ _            _          ___    _____                    #
#                   |_   _| __ __ _  ___ ___  __ _| |__ (_) (_) |_ _   _   (_)_ __    |_ _|__|_   _|                   #
#                     | || '__/ _` |/ __/ _ \/ _` | '_ \| | | | __| | | |  | | '_ \    | |/ _ \| |                     #
#                     | || | | (_| | (_|  __/ (_| | |_) | | | | |_| |_| |  | | | | |   | | (_) | |                     #
#                     |_||_|  \__,_|\___\___|\__,_|_.__/|_|_|_|\__|\__, |  |_|_| |_|  |___\___/|_|                     #
#                                                                  |___/                                               #
#                                                                                                                      #
#                                                                                                                      #
#        PROJECT:     Hyot                                                                                             #
#           FILE:     hyot_main.py                                                                                     #
#                                                                                                                      #
#          USAGE:     sudo python hyot_main.py                                                                         #
#                                                                                                                      #
#    DESCRIPTION:     This component monitors several events -distance, temperature and humidity- of the environment   #
#                     from sensors connected to a Raspberry Pi and in case of an anomalous reading, the alert protocol #
#                     is activated                                                                                     #
#                                                                                                                      #
#        OPTIONS:     Type '-h' or '--help' option to show the help                                                    #
#   REQUIREMENTS:     Root user, GNU/Linux platform, Connection to the network, Connected devices: DTH11 and HC-SR04   #
#                     sensors, Modules:                                                                                #
#                           - camera_module.py                  - gpg_module.py                                        #
#                           - checks_module.py                  - hyperledgerFabric_module.py                          #
#                           - cloudantdb_module.py              - iot_module.py TODO IBM Cloud - IoT Platform          #
#                           - dropbox_module.py                 - lcd_module.py                                        #
#                           - email_module.py                   - system_module.py                                     #
#                           - logger.py                                                                                #
#                                                                                                                      #
#          NOTES:     It must be run with root user on a Raspberry Pi preferably with Raspbian as operating system     #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.1                                                                                            #
#        CREATED:     12/27/17                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This component monitors several events -distance, temperature and humidity- of the environment from sensors connected
   to a Raspberry Pi and in case of an anomalous reading, the alert protocol is activated"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import Adafruit_DHT                             # DHT11 sensor
    import camera_module as picamera                # Module to handle the Picamera
    import checks_module as checks                  # Module to execute initial checks and to parse the menu
    import cloudantdb_module as cloudantdb          # Module that contains the logic of the Cloudant NoSQL DB service
    import datetime                                 # Basic date and time types
    import dropbox_module as dropbox                # Module that contains the logic of the Dropbox service
    import email_module as email                    # Module to send emails
    import gpg_module as gpg                        # Module that contains the logic of the functionality of GPG
    import hyperledgerFabric_module as hlf          # Module that contains the logic to use Hyperledger Fabric
    # import iot_module as iot                      # Module that contains the logic of the IoT platform TODO IBM Cloud - IoT Platform
    import lcd_module as lcd                        # Module to handle the LCDs
    import logger as logger                         # Class to redirect stdout to both file and console
    import system_module as system                  # Module that performs functions in the local operating system
    import time                                     # Time access and conversions
    import traceback                                # Print or retrieve a stack traceback
    import uuid                                     # UUID objects according to RFC 4122
    from colorama import Fore, Style                # Cross-platform colored terminal text
    from gpiozero import LED, DistanceSensor        # Simple interface to GPIO devices

except ImportError as importError:
    print("Error to import in hyot_main: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
def constants(user_args):
    """
    Contains all definitions of constants.

    :param user_args: Values of the options entered by the user.
    """

    global SENSORS, DHT11_EVENTS, HCSR_EVENTS, MAILTO, WAIT_TIME_MEASUREMENT, DHT_SENSOR, DHT_PINDATA, TEMP_THRESHOLD,\
        HUM_THRESHOLD, ALERT_LED, HCSR_SENSOR, HCSR_MAXDISTANCE, DISTANCE_THRESHOLD, EXT, DHT_SENSOR_NAME,\
        HCSR_SENSOR_NAME, TEMPERATURE_TEXT, HUMIDITY_TEXT, DISTANCE_TEXT

    try:
        SENSORS = ["DHT11", "HCSR04"]                               # Name of the sensors
        DHT11_EVENTS = ["Temperature", "Humidity"]                  # Name of the events of the DHT11 sensor
        HCSR_EVENTS = ["Distance"]                                  # Name of the events of the HC-SR04 sensor
        MAILTO = user_args.EMAIL                                    # Recipient's email address
        WAIT_TIME_MEASUREMENT = user_args.WAITTIME_MEASUREMENT      # Wait time between each measurement. Default 3 seconds
        DHT_SENSOR = Adafruit_DHT.DHT11                             # DHT11 sensor
        DHT_PINDATA = user_args.DHT_DATAPIN                         # DHT11 - Data pin. Default 21 (GPIO21)
        TEMP_THRESHOLD = user_args.TEMPERATURE_THRESHOLD            # Temperature alert threshold in the DHT11 sensor
        HUM_THRESHOLD = user_args.HUMIDITY_THRESHOLD                # Humidity alert threshold in the DHT11 sensor
        ALERT_LED = LED(user_args.LED_PIN)                          # Led pin. Default 13 (GPIO13)
        # HC-SR04 sensor. Default pins: echo GPIO19, trigger GPIO26. Default maximum distance to be measured: 1.5 meters
        HCSR_SENSOR = DistanceSensor(echo=user_args.HCSR_ECHOPIN,
                                     trigger=user_args.HCSR_TRIGPIN,
                                     max_distance=user_args.HCSR_MAXDISTANCE)
        HCSR_MAXDISTANCE = user_args.HCSR_MAXDISTANCE               # Maximum distance to be measured (HC-SR04 sensor)
        DISTANCE_THRESHOLD = user_args.DISTANCE_THRESHOLD           # Distance alert threshold in the HC-SR04 sensor
        EXT = '.h264'                                               # Extension of the video file
        DHT_SENSOR_NAME = "DHT11 sensor"                            # Text - DHT11 sensor name
        HCSR_SENSOR_NAME = "HC-SR04 sensor"                         # Text - HC-SR04 sensor name
        TEMPERATURE_TEXT = "Temperature: "                          # Text - Temperature event
        HUMIDITY_TEXT = "Humidity: "                                # Text - Humidity event
        DISTANCE_TEXT = "Distance: "                                # Text - Distance event

    except Exception as exception:
        print(Fore.RED + "\n✖ Exception in constants() function: " + str(exception) + ".")
        # Prints the traceback
        traceback.print_exc()
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\r" + Fore.RED + "✖ Exception: KeyboardInterrupt. Please, do not interrupt the execution." + Fore.RESET)
        sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
uuid_measurement = None                     # UUID of each measurement for both sensors
datetime_measurement = None                 # Datetime in which the measurement was taken
video_filename = None                       # Name of the video file
video_filefullpath = None                   # Full path of the recording
recording_time = None                       # Time that the recording will take
alert_triggered = None                      # Indicates if an alert has been triggered
threshold_value = None                      # Indicates the value of the event threshold that triggers the alert
link = None                                 # Link of the uploaded file to the Cloud (e.g. Dropbox)
hash_code = None                            # Hash code of the video file


########################################
#               FUNCTIONS              #
########################################
def header():
    """
    Prints the header by console.
    """

    banner = """
    _    ___     ______ _______
   | |  | \ \   / / __ \__   __|
   | |__| |\ \_/ / |  | | | |
   |  __  | \   /| |  | | | |
   | |  | |  | | | |__| | | |
   |_|  |_|  |_|  \____/  |_|


   A PoC for traceability in IoT environments through Hyperledger Fabric by:

   - Jesús Iglesias García, jesusgiglesias@gmail.com

   -----------------------------------------------------

   HYOT - TRACEABILITY IN IoT

   This component monitors several events -distance, temperature and humidity- of the environment from 
   sensors connected to a Raspberry Pi and in case of an anomalous reading, the alert protocol is activated.
   
   Type the '-h' or '--help' option to get more information.

   """

    # Header
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + banner + Style.RESET_ALL)

    # Wait time - 1 second
    time.sleep(1)


def timestamp():
    """
    Generates a timestamp string for each measurement and for each video taken.
    """

    return datetime.datetime.now()


def information_values():
    """
    Shows the information by console about some values established.
    """

    global TEMP_THRESHOLD, HUM_THRESHOLD, DISTANCE_THRESHOLD, WAIT_TIME_MEASUREMENT, HCSR_MAXDISTANCE, recording_time

    print(Style.BRIGHT + Fore.BLACK + "\n   -- Information - Values established:" + Style.RESET_ALL)
    # Information about the current thresholds
    print(Fore.BLACK + "      -- Alert thresholds:")
    print("        - Sensor: DHT11   | Event: Temperature | > " + str(TEMP_THRESHOLD) + " °C")
    print("        - Sensor: DHT11   | Event: Humidity    | > " + str(HUM_THRESHOLD) + " %")
    print("        - Sensor: HC-SR04 | Event: Distance    | < " + str(DISTANCE_THRESHOLD) + " cm")
    # Information about the recording time
    print("      -- Recording time: " + str(recording_time) + " seconds")
    # Information about the time between measurements
    print("      -- Time between measurements: " + str(WAIT_TIME_MEASUREMENT) + " seconds")
    # Information about the maximum distance to be measured by the HC-SR04 sensor
    print("      -- Maximum distance to be measured (HC-SR04): " + str(HCSR_MAXDISTANCE) + " meters" + Fore.RESET)

    time.sleep(2)


def reset_values():
    """
    Resets the value of the global variables.
    """

    global video_filename, video_filefullpath, alert_triggered, threshold_value, link, hash_code

    video_filename = None
    video_filefullpath = None
    alert_triggered = False
    threshold_value = None
    link = None
    hash_code = None


def add_cloudant(sensor, event, temperature, humidity, distance, owner):
    """
    Adds the data to the Cloudant NoSQL database.

    :param sensor: Indicates the sensor that triggered the alert.
    :param event: Indicates the event that triggered the alert.
    :param temperature: Indicates the value of measured temperature.
    :param humidity: Indicates the value of measured humidity.
    :param distance: Indicates the value of measured distance.
    :param owner: Indicates the participant who registers the transaction in the Blockchain.
    """

    global MAILTO, uuid_measurement, datetime_measurement, alert_triggered, threshold_value, link

    # Creates a JSON document content data
    data = {
        '_id': str(uuid_measurement),
        "datetime_field": str(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p")),
        "temperature_field": temperature,
        "humidity_field": humidity,
        "distance_field": distance,
        "alert_triggered": alert_triggered,
        "sensor_origin": sensor,
        "event_origin": event,
        "threshold_value": threshold_value,
        "link": link,
        "mailto": MAILTO,
        "owner": owner
    }

    # Adds the document to the database of the Cloudant NoSQL service
    cloudantdb.add_document(data, MAILTO)


def alert_protocol(sensor, event, temperature, humidity, distance):
    """
    Initiates the alert protocol.

    :param sensor: Indicates the sensor that triggered the alert.
    :param event: Indicates the event that triggered the alert.
    :param temperature: Indicates the value of measured temperature.
    :param humidity: Indicates the value of measured humidity.
    :param distance: Indicates the value of measured distance.
    """

    global MAILTO, ALERT_LED, EXT, uuid_measurement, datetime_measurement, video_filename, video_filefullpath,\
        recording_time, alert_triggered, threshold_value, link, hash_code

    # Name of the video file
    video_filename = sensor.lower() + '_' + event.lower() + '_' + str(datetime_measurement.strftime("%d%m%Y_%H%M%S")) \
                     + EXT

    # Full path of the video file
    video_filefullpath = system.tempfiles_path + '/' + video_filename

    alert_triggered = True                                              # Marks the alert like triggered
    time.sleep(1)
    lcd.clear_lcd(sensor)                                               # Clears the LCD
    time.sleep(1)

    print(Fore.RED + "   ---------- ALERT TRIGGERED | " + sensor + " | " + event + " ----------  " + Fore.RESET)
    lcd.full_print_lcd(sensor, "ALERT TRIGGERED!", event)
    ALERT_LED.on()                                                      # Turns on the red led
    time.sleep(5)

    lcd.clear_lcd(sensor)                                               # Clears the LCD
    print(Fore.BLACK + "   ----------- Initiating the alert protocol ------------  " + Fore.RESET)
    lcd.full_print_lcd(sensor, "Initiating the", "protocol...")

    # Takes a recording for n seconds (default 10 seconds). This recording is the evidence
    picamera.record_video(video_filefullpath, recording_time, MAILTO)

    # Checks if the original evidence exists in the local system
    system.check_file(video_filefullpath, MAILTO)

    # Applies a hash function to the content of the evidence (decrypted file)
    hash_code = hlf.file_hash(video_filefullpath, MAILTO)

    # Encrypts the evidence
    final_path = gpg.encrypt_sign_file(video_filefullpath, MAILTO)

    # Checks if the encrypted evidence exists in the local system
    system.check_file(final_path, MAILTO)

    # Uploads the encrypted evidence to the Cloud (e.g. Dropbox)
    link = dropbox.upload_file(final_path, sensor, MAILTO)

    # Publishes the event in the IoT platform TODO IBM Cloud - IoT Platform
    # iot.publish_event(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p"), temperature, humidity, distance, MAILTO)

    # Adds the current measurement to the database
    add_cloudant(sensor, event, temperature, humidity, distance, hlf.owner_alert)

    # Submits the transaction to Hyperledger Fabric to publish a new alert asset
    hlf.publishAlert_transaction(str(uuid_measurement), datetime_measurement, sensor, event, hash_code, link, MAILTO)

    # Sends an email when an alert is triggered
    if not (MAILTO is None):
        email.send_email(MAILTO, str(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p")), str(uuid_measurement),
                         temperature, humidity, distance, link, sensor, event, threshold_value)

    # Removes the temporary file (original evidence)
    system.remove_file(video_filefullpath, False)

    # Encryption had success
    if video_filefullpath != final_path:
        # Removes the temporary file (encrypted evidence) after uploading to the Cloud (e.g. Dropbox)
        system.remove_file(final_path, True)

    time.sleep(1)
    lcd.clear_lcd(sensor)                                       # Clears the LCD
    ALERT_LED.off()                                             # Turns off the red led
    time.sleep(1)
    print(Fore.RED + "   ----------- PROTOCOL FINISHED. CONTINUING... ----------  " + Fore.RESET)
    lcd.full_print_lcd(sensor, "Protocol", "finished...")


def print_data_measurement():
    """
    Prints the UUID and datetime of each measurement.
    """

    global datetime_measurement, uuid_measurement

    print(Style.BRIGHT + "   UUID: " + Style.RESET_ALL + str(uuid_measurement))
    print("   Datetime: " + str(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p")))


def no_alert_protocol(temperature, humidity, distance):
    """
    Steps to perform when an alert is not triggered.

    :param temperature: Value of this event in the current measurement.
    :param humidity: Value of this event in the current measurement.
    :param distance: Value of this event in the current measurement.
    """

    global MAILTO, datetime_measurement

    # Publishes the event in the IoT platform TODO IBM Cloud - IoT Platform
    # iot.publish_event(datetime_measurement.strftime("%d-%m-%Y %H:%M:%S %p"), temperature, humidity, distance, MAILTO)

    # Adds the measurement to the database
    add_cloudant(None, None, temperature, humidity, distance, hlf.owner_alert)


def check_invalid_values_dht11(temperature, humidity, distance):
    """
    Checks the values of the DHT11 sensor when some is invalid.

    :param temperature: Value of this event in the current measurement.
    :param humidity: Value of this event in the current measurement.
    :param distance: Value of this event in the current measurement.
    """

    global SENSORS, HCSR_EVENTS, DISTANCE_THRESHOLD, DHT_SENSOR_NAME, HCSR_SENSOR_NAME, DISTANCE_TEXT, threshold_value

    # Prints the UUID and datetime of each measurement
    print_data_measurement()

    print(Style.BRIGHT + Fore.BLACK + "   " + DHT_SENSOR_NAME + Style.RESET_ALL)

    # Checks that event is invalid
    if temperature is None and humidity is None:
        print("   Failed to get reading. Humidity and temperature are invalid or None.")

    elif humidity is None:
        print("   Failed to get reading. Humidity is invalid or None.")

    elif temperature is None:
        print("   Failed to get reading. Temperature is invalid or None.")

    # Shows the LCD as empty - DHT11 sensor
    lcd.print_measure_dht(None, None, True, True)

    print(Style.BRIGHT + Fore.BLACK + "   " + HCSR_SENSOR_NAME + Style.RESET_ALL)
    print("   " + DISTANCE_TEXT + " {0:0.3f} cm \n".format(distance) + Fore.RESET)

    # Outputs the data by LCD
    lcd.print_measure_hcsr(distance, False)

    # Alert - HC-SR04 | Distance
    if distance < DISTANCE_THRESHOLD:
        threshold_value = DISTANCE_THRESHOLD
        alert_protocol(SENSORS[1], HCSR_EVENTS[0], temperature, humidity, distance)
    # No alert
    else:
        no_alert_protocol(temperature, humidity, distance)


def main(user_args):
    """
    Main function.

    :param user_args: Values of the options entered by the user.
    """

    # Try-Catch block
    try:

        global SENSORS, MAILTO, WAIT_TIME_MEASUREMENT, DHT_SENSOR, DHT_PINDATA, DHT11_EVENTS, TEMP_THRESHOLD,\
            HUM_THRESHOLD, HCSR_SENSOR, HCSR_EVENTS, HCSR_MAXDISTANCE, DISTANCE_THRESHOLD, DHT_SENSOR_NAME,\
            HCSR_SENSOR_NAME, TEMPERATURE_TEXT, HUMIDITY_TEXT, DISTANCE_TEXT, uuid_measurement, datetime_measurement,\
            recording_time, threshold_value

        # Variables
        count = 0                                           # Measurement counter
        recording_time = user_args.RECORDING_TIME           # Time of recording

        # Header
        header()

        # ############### Initializing HYOT ###############
        print(Style.BRIGHT + Fore.BLACK + "   -- Initializing HYOT..." + Style.RESET_ALL)

        # ############### Initializing LCDs ###############
        lcd.init(user_args.DHT_I2CEXPANDER, user_args.DHT_I2CADDRESS, user_args.HCSR_I2CEXPANDER,
                 user_args.HCSR_I2CADDRESS, SENSORS)  # Initializes the LCD instances

        # ############### Initializing the Picamera ###############
        picamera.init()                             # Initializes the Picamera

        # ############### Initializing local directory ###############
        system.create_localdir()                    # Creates a local directory to store the files taken by the Picamera

        # ############### Initializing GPG ###############
        gpg.init()                                  # Creates the GPG instance and the public and private keys

        # ############### Initializing the mail session ###############
        if not (MAILTO is None):
            email.init()                            # Initializes the mail session

        # ############### Initializing IoT Platform TODO IBM Cloud - IoT Platform ###############
        # iot.connect()                             # Creates the IoT client and establishes a connection

        # ############### Initializing databases (Cloudant NoSQL DB) ###############
        cloudantdb.connect()                        # Creates a Cloudant DB client and establishes a connection
        cloudantdb.init(timestamp())                # Initializes the database

        # ############### Initializing Dropbox ###############
        dropbox.connect()                           # Creates a Dropbox client and establishes a connection
        dropbox.init(SENSORS)                       # Initializes the main directory and subdirectories

        # ############### Initializing Hyperledger Fabric ###############
        hlf.init()                                  # Checks if Hyperledger Fabric is alive

        time.sleep(2)                               # Wait time - 2 seconds
        lcd.clear_lcds()                            # Clears both LCDs
        time.sleep(1)                               # Wait time - 1 second

        # ############### Information - Values established ###############
        information_values()

        # ############### Reading values ###############
        print(Style.BRIGHT + Fore.BLACK + "\n   -- Reading values each " + str(WAIT_TIME_MEASUREMENT) + " seconds from "
              "sensors\n" + Style.RESET_ALL)

        lcd.full_print_lcds("Reading values", "from sensors")           # Writes in both LCDS using both rows
        time.sleep(1)
        lcd.clear_lcds()
        time.sleep(1)

        # DHT11 and HC-SR04 sensors
        lcd.print_lcds("- " + DHT_SENSOR_NAME + " -", " " + HCSR_SENSOR_NAME + " ")
        time.sleep(2)
        lcd.clear_lcds()

        # Loops each n seconds (default 3 seconds). This is the time between each measurement
        while True:

            # If an alert has been triggered, the LCDs are cleared
            if alert_triggered:
                lcd.clear_lcds()

            count += 1                                                  # Increments the counter
            datetime_measurement = timestamp()                          # Obtains a timestamp (datetime)
            uuid_measurement = uuid.uuid4()                             # Generates a random UUID
            reset_values()                                              # Resets the values

            print(Style.BRIGHT + Fore.CYAN + "   Measurement %i" % count + Style.RESET_ALL)

            # Obtains the humidity and temperature
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PINDATA)
            # Obtains the distance (3 decimals)
            distance = round(HCSR_SENSOR.distance * 100, 3)

            # All events are invalid
            if (humidity is None or 0 > humidity > 100) and (temperature is None or temperature < 0) and \
               (distance is None or distance < 0 or distance > HCSR_MAXDISTANCE * 100):

                print("   Failed to get reading. All events have invalid values.")

                # Shows the LCDs as empty
                lcd.print_measure_dht(None, None, True, True)
                lcd.print_measure_hcsr(None, True)

            # Humidity and temperature values are invalid or None
            elif (humidity is None or 0 > humidity > 100) and (temperature is None or temperature < 0) and \
                    (distance is not None and 0 <= distance <= HCSR_MAXDISTANCE * 100):

                temperature = None                                              # Invalid value
                humidity = None                                                 # Invalid value
                check_invalid_values_dht11(temperature, humidity, distance)     # Checks the value

            # Humidity value is invalid or None
            elif (humidity is None or 0 > humidity > 100) and (temperature is not None and temperature >= 0 and
                                                               distance is not None and
                                                               0 <= distance <= HCSR_MAXDISTANCE * 100):

                humidity = None                                                 # Invalid value
                check_invalid_values_dht11(temperature, humidity, distance)     # Checks the value

            # Temperature value is invalid or None
            elif (temperature is None or temperature < 0) and (humidity is not None and 0 <= humidity <= 100 and
                                                               distance is not None and
                                                               0 <= distance <= HCSR_MAXDISTANCE * 100):

                temperature = None                                              # Invalid value
                check_invalid_values_dht11(temperature, humidity, distance)     # Checks the value

            # Distance value is invalid, None or upper than maximum distance
            elif (distance is None or distance < 0 or distance > HCSR_MAXDISTANCE * 100) and (humidity is not None and
                                                                                              0 <= humidity <= 100 and
                                                                                              temperature is not None
                                                                                              and temperature >= 0):

                distance = None                                     # Invalid value
                print_data_measurement()                            # Prints the UUID and datetime of each measurement

                print(Style.BRIGHT + Fore.BLACK + "   " + DHT_SENSOR_NAME + Style.RESET_ALL)
                print("   " + TEMPERATURE_TEXT + " {0:0.1f} °C \n   ".format(temperature) + HUMIDITY_TEXT +
                      " {0:0.1f} %".format(humidity) + Fore.RESET)

                # Outputs the data by LCD
                lcd.print_measure_dht(temperature, humidity, False, False)

                print(Style.BRIGHT + Fore.BLACK + "   " + HCSR_SENSOR_NAME + Style.RESET_ALL)
                print("   Failed to get reading. Distance is invalid, None or upper than the maximum distance.")
                lcd.print_measure_hcsr(None, True)

                # Alert - DHT11 | Temperature
                if temperature > TEMP_THRESHOLD:
                    threshold_value = TEMP_THRESHOLD
                    alert_protocol(SENSORS[0], DHT11_EVENTS[0], temperature, humidity, distance)

                # Alert - DHT11 | Humidity
                elif humidity > HUM_THRESHOLD:
                    threshold_value = HUM_THRESHOLD
                    alert_protocol(SENSORS[0], DHT11_EVENTS[1], temperature, humidity, distance)

                # No alert
                else:
                    no_alert_protocol(temperature, humidity, distance)

            # All values are valid
            else:

                # Prints the UUID and datetime of each measurement
                print_data_measurement()

                print(Style.BRIGHT + Fore.BLACK + "   " + DHT_SENSOR_NAME + Style.RESET_ALL)
                print("   " + TEMPERATURE_TEXT + " {0:0.1f} °C \n   ".format(temperature) + HUMIDITY_TEXT +
                      " {0:0.1f} %".format(humidity) + Fore.RESET)

                # Outputs the data by LCD
                lcd.print_measure_dht(temperature, humidity, False, False)

                print(Style.BRIGHT + Fore.BLACK + "   " + HCSR_SENSOR_NAME + Style.RESET_ALL)
                print("   " + DISTANCE_TEXT + " {0:0.3f} cm \n".format(distance) + Fore.RESET)

                # Outputs the data by LCD
                lcd.print_measure_hcsr(distance, False)

                # Alert - DHT11 | Temperature
                if temperature > TEMP_THRESHOLD:
                    threshold_value = TEMP_THRESHOLD
                    alert_protocol(SENSORS[0], DHT11_EVENTS[0], temperature, humidity, distance)

                # Alert - DHT11 | Humidity
                elif humidity > HUM_THRESHOLD:
                    threshold_value = HUM_THRESHOLD
                    alert_protocol(SENSORS[0], DHT11_EVENTS[1], temperature, humidity, distance)

                # Alert - HC-SR04 | Distance
                elif distance < DISTANCE_THRESHOLD:
                    threshold_value = DISTANCE_THRESHOLD
                    alert_protocol(SENSORS[1], HCSR_EVENTS[0], temperature, humidity, distance)

                # No alert
                else:
                    no_alert_protocol(temperature, humidity, distance)

            print("\n   -----------------------------\n")

            time.sleep(WAIT_TIME_MEASUREMENT - 1)

    except IOError as ioError:                      # Related to LCD 16x2 and Cloudant NoSQL DB
        print(Fore.RED + "\n   ✖ IOError in the main() function or in the modules: " + str(ioError) + ". Main reasons:")
        print("     - LCD - I2C protocol")
        print("       Errno 2: I2C interface is disabled.\r")
        print("       Errno 22: I2C address is invalid.\r")
        print("       Errno 121: LCD is not connected.\r")
        sys.exit(1)
    except Exception as exception:
        print(Fore.RED + "\n   ✖ Exception in the main() function or in the modules: " + str(exception.message.lower())
              + ".")
        # Prints the traceback
        traceback.print_exc()
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n   ✖ Exception: KeyboardInterrupt." + Fore.RESET)
        sys.exit(1)
    finally:
        print(Style.BRIGHT + Fore.BLACK + "\n   -- Ending HYOT..." + Style.RESET_ALL)
        try:
            print("\r")
            lcd.disconnect_lcds()                       # Disconnects the LCDs
            picamera.disconnect()                       # Disconnects the Picamera
            system.remove_localdir()                    # Removes the temporary local directory
            gpg.clean()                                 # Cleans the GPG instance
            email.disconnect()                          # Disconnects the mail session
            # iot.disconnect()                          # Disconnects the IoT client TODO IBM Cloud - IoT Platform
            cloudantdb.disconnect()                     # Disconnects the Cloudant client
            dropbox.disconnect()                        # Disables the access token used to authenticate the calls
            print("\r")
        except Exception as finallyException:
            print(Fore.RED + "\n   ✖ Exception in the finally statement of the main() function: " +
                  str(finallyException.message.lower()) + ".")
            # Prints the traceback
            traceback.print_exc()
            print(Fore.RESET)
            sys.exit(1)


########################################
#             MAIN PROGRAM             #
########################################
if __name__ == '__main__':

    checks.check_root()                             # Function to check the user
    checks.check_platform()                         # Checks if the component is run on GNU/Linux platform
    checks.check_raspberrypi()                      # Checks if the component is run on a Raspberry Pi
    checks.check_network()                          # Checks if the Raspberry Pi is connected to the network
    checks.check_concurrency()                      # Checks if the component is or not already running

    logfile = system.create_logger_dir()            # Creates the directory for logging file
    logger.start(logfile)                           # Starts the logger

    arguments = checks.menu()                       # Checks the options entered by the user when running the component
    constants(arguments)                            # Declares all the constants
    main(arguments)                                 # Main function
