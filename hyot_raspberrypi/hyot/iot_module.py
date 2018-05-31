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
#           FILE:     iot_module.py                                                                                    #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic of the Internet of Things platform (IBM Cloud service)            #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Account in the IBM Cloud service. Raspberry Pi device connected to the platform. Events, which   #
#                     will be sent, must be defined in the platform                                                    #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/29/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic of the Internet of Things platform (IBM Cloud service)"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                    # System-specific parameters and functions
    import time                                   # Time access and conversions
    import logging                                # Logging facility for Python
    import yaml                                   # YAML parser and emitter for Python
    from colorama import Fore, Style              # Cross-platform colored terminal text
    import ibmiotf.device                         # Module for interacting with the IBM Cloud IoT Platform

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
    print(Fore.RED + "Please, place the configuration file (hyot.yml) inside a directory called conf in the root "
                     "path (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)
except yaml.YAMLError as yamlError:
    print(Fore.RED + "The configuration file (conf/hyot.yml) has not the YAML format." + Fore.RESET)
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
    print(Fore.RED + "Please, make sure that the keys: [iot|orgid], [iot|devicetype], [iot|deviceid], [iot|authmethod] "
                     "and [iot|authtoken] exist in the configuration file (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
client = None                                     # IoT platform client


########################################
#               FUNCTIONS              #
########################################
def connect():
    """Creates the IoT client and establishes a connection"""

    global ORGID, DEVICETYPE, DEVICEID, AUTHTOKEN, AUTHMETHOD, client

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Generating the client of the IoT Platform"
          + Style.RESET_ALL)

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
        print(Fore.RED + "        The IoT platform credentials can not be empty" + Fore.RESET)
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

        print(Fore.GREEN + "        IoT platform client connected" + Fore.RESET)

    except Exception as iotError:
        print(Fore.RED + "        Error to initialize the IoT client. Exception: " + Fore.RESET + str(iotError))
        sys.exit(1)

    time.sleep(1)
    print("\n        ------------------------------------------------------")


def publish_event(timestamp, temperature, humidity, distance):
    """Sends the event to the IoT platform
    :param timestamp: Date and time when the measurement was taken
    :param temperature: Value of this event in the current measurement
    :param humidity: Value of this event in the current measurement
    :param distance: Value of this event in the current measurement
    """

    global client

    # Data to send to the IoT platform
    data = {'d': {'Datetime': timestamp, 'Temperature': temperature, 'Humidity': humidity, 'Distance': distance}}

    try:
        print(Fore.LIGHTBLACK_EX + "   -- Publishing the event to the IoT platform" + Fore.RESET),
        time.sleep(0.5)

        # Sends the data to the Watson IoT Platform
        client.publishEvent('event', 'json', data)

        print(Fore.GREEN + " ✓" + Fore.RESET)

    except Exception as publishError:
        print(Fore.RED + " ✕ Error publishing the event: " + str(publishError) + Fore.RESET)


def disconnect():
    """Disconnects the IoT platform client"""

    global client

    if not (client is None):
        print("        Disconnecting the IoT platform client"),

        time.sleep(0.25)

        try:
            client.disconnect()                   # Ends the client session
            client = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
