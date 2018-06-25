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
#           FILE:     iot_module.py                                                                                    #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic of the Internet of Things platform (IBM Cloud service)            #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Account in the IBM Cloud service, Raspberry Pi device connected to the platform, Events, which   #
#                     will be sent, must be defined on the platform, Connection to the network                         #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     01/29/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic of the Internet of Things platform (IBM Cloud service)"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                    # System-specific parameters and functions
    import email_module as email                  # Module to send emails
    import ibmiotf.device                         # Module for interacting with the IBM Cloud IoT Platform
    import logging                                # Logging facility for Python
    import time                                   # Time access and conversions
    import yaml                                   # YAML parser and emitter for Python
    from colorama import Fore, Style              # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in iot_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#       LOAD YAML CONFIGURATION        #
########################################
conf = None
try:
    conf = yaml.load(open('conf/hyot.yml'))

except IOError as ioERROR:
    print(Fore.RED + "✖ Please, place the configuration file (hyot.yml) inside a directory called 'conf' in the root "
                     "path (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)
except yaml.YAMLError as yamlError:
    print(Fore.RED + "✖ The configuration file (conf/hyot.yml) has not the YAML format." + Fore.RESET)
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
try:
    ORGID = conf['iot']['orgid']                  # Identifier of the organization
    DEVICETYPE = conf['iot']['devicetype']        # Type of device. It is a grouping for devices that perform a task
    DEVICEID = conf['iot']['deviceid']            # Unique identifier of the device (normally the MAC address)
    AUTHMETHOD = conf['iot']['authmethod']        # Method of authentication
    AUTHTOKEN = conf['iot']['authtoken']          # Authentication token to securely connect the device to the platform
except (KeyError, TypeError) as keyError:
    print(Fore.RED + "✖ Please, make sure that the keys: [iot|orgid], [iot|devicetype], [iot|deviceid],"
                     " [iot|authmethod] and [iot|authtoken] exist in the configuration file (conf/hyot.yml)."
          + Fore.RESET)
    sys.exit(1)

# Name to identify the step where the error has occurred
STEP_IOTPLATFORM = "Publish event in IoT Platform"

########################################
#           GLOBAL VARIABLES           #
########################################
client = None                                     # IoT platform client


########################################
#               FUNCTIONS              #
########################################
def connect():
    """
    Creates the IoT client and establishes a connection.
    """

    global ORGID, DEVICETYPE, DEVICEID, AUTHTOKEN, AUTHMETHOD, client

    print(Style.BRIGHT + Fore.BLACK + "\n      - Generating the client of the IoT Platform" + Style.RESET_ALL)

    # Asks the user for IoT platform credentials
    organization_id = raw_input(Fore.BLUE + "        Enter the identifier of the organization: " + Fore.WHITE + "(" +
                                ORGID + ") " + Fore.RESET) or ORGID
    device_type = raw_input(Fore.BLUE + "        Enter the type of device: " + Fore.WHITE + "(" + DEVICETYPE + ") "
                            + Fore.RESET) or DEVICETYPE
    device_id = raw_input(Fore.BLUE + "        Enter the identifier of the device: " + Fore.WHITE + "(" + DEVICEID +
                          ") " + Fore.RESET) or DEVICEID

    auth_token = raw_input(Fore.BLUE + "        Enter the authentication token or empty to use the default value: "
                           + Fore.RESET) or AUTHTOKEN

    # Checks if some field is empty
    if organization_id.isspace() or device_type.isspace() or device_id.isspace() or auth_token.isspace():
        print(Fore.RED + "        ✖ The IoT platform credentials can not be empty." + Fore.RESET)
        sys.exit(0)

    try:
        # Debugger - Threshold: ERROR level
        logger = logging.getLogger('wiotp.deviceconnstate')
        logger.setLevel(logging.ERROR)
        output = logging.StreamHandler(stream=None)
        output.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        output.setFormatter(formatter)
        logger.addHandler(output)

        options = {
            "org": organization_id.replace(" ", ""),
            "type": device_type.replace(" ", ""),
            "id": device_id.replace(" ", ""),
            "auth-method": AUTHMETHOD,
            "auth-token": auth_token.replace(" ", ""),
            "clean-session": True
        }

        # Initializes the device client
        client = ibmiotf.device.Client(options, logHandlers=output)

        # Establishes a connection with the service instance
        client.connect()
        print(Fore.GREEN + "        ✓ IoT platform client connected" + Fore.RESET)

    except Exception as iotError:
        print(Fore.RED + "        ✖ Error to initialize the IoT client. Exception: " + str(iotError) + "." + Fore.RESET)
        sys.exit(1)

    time.sleep(1)
    print("\n        ------------------------------------------------------")


def publish_event(timestamp, temperature, humidity, distance, mailto):
    """
    Sends the event to the IoT platform.

    :param timestamp: Date and time when the measurement was taken.
    :param temperature: Value of this event in the current measurement.
    :param humidity: Value of this event in the current measurement.
    :param distance: Value of this event in the current measurement.
    :param mailto: Email address where to send the error notification if it occurs.
    """

    global STEP_IOTPLATFORM, client

    # Data to send to the IoT platform
    data = {'d': {'Datetime': timestamp, 'Temperature': temperature, 'Humidity': humidity, 'Distance': distance}}

    try:
        print(Fore.LIGHTBLACK_EX + "     -- Publishing the event to the IoT platform" + Fore.RESET),
        time.sleep(0.5)

        # Sends the data to the Watson IoT Platform
        client.publishEvent('event', 'json', data)

        print(Fore.GREEN + " ✓" + Fore.RESET)

    except Exception as publishError:
        print(Fore.RED + " ✖ Error publishing the event in IoT Platform. Exception: " + str(publishError) + ".\n"
              + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert procedure
        email.print_error_notification_or_send_email(mailto, STEP_IOTPLATFORM)

        sys.exit(1)


def disconnect():
    """
    Disconnects the IoT platform client.
    """

    global client

    if not (client is None):
        print("      Disconnecting the IoT platform client"),

        time.sleep(0.25)

        try:
            client.disconnect()                   # Ends the client session
            client = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
