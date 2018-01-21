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
#           FILE:     dropbox_module.py                                                                                #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic of the Dropbox service                                            #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Account in the Dropbox service                                                                   #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/08/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic of the Dropbox service"""

########################################
#               IMPORTS                #
########################################

try:
    import sys                                          # System-specific parameters and functions
    import time                                         # Time access and conversions
    from colorama import Fore, Style                    # Cross-platform colored terminal text
    import dropbox                                      # Python SDK for integrating with the Dropbox API v2

except ImportError as importError:
    print("Error to import in dropbox_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
SENSORS = ["DHT11", "HC-SR04"]                                              # Name of the sensors
HYOT_DIR = "Hyot"                                                           # Name of the main directory
DHT11_DIR = "dht11_images"                                                  # Name of the DHT11 sensor subdirectory TODO - Images?
HCSR04_DIR = "hcsr04_images"                                                # Name of the HC-SR04 sensor subdirectory TODO - Images?
TOKEN = "eI5UZqDlaNAAAAAAAAAAJm2xSwyCoMquSwWq7p270YXf5qr3p1vawOu5AzS99Uih"  # Authorisation token
MIN_SPACE = 524288000                                                       # Recommended available space in the account (500 MB = 524288000 bytes)


########################################
#           GLOBAL VARIABLES           #
########################################
dbx = None                  # Instance of a Dropbox class
path = None                 # Path where create folders or upload files
message_dir = None          # Message
dht_subdir = None           # Final name of the DHT11 sensor subdirectory (default value or value entered by the user)
hcsr_subdir = None          # Final name of the HC-SR04 sensor subdirectory (default value or value entered by the user)


########################################
#               FUNCTIONS              #
########################################
def connect():
    """Creates an instance of the Dropbox class and establishes a connection"""

    global dbx

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Generating the client of the Dropbox service" + Style.RESET_ALL)

    # Asks the user for Dropbox token
    token = raw_input(Fore.BLUE + "        Enter the Dropbox token or empty to use the default value: "
                      + Fore.RESET) or TOKEN

    # Checks if the Dropbox token is empty
    if token.isspace():
        print(Fore.RED + "        The Dropbox token can not be empty" + Fore.RESET)
        sys.exit(1)

    # Creates an instance of the Dropbox class, which can make requests to API
    dbx = dropbox.Dropbox(token.replace(" ", ""))

    try:

        # Checks that the access token is valid
        current_user = dbx.users_get_current_account()

        print(Fore.GREEN + "        Dropbox client connected with the user: " + current_user.name.given_name
              + Fore.RESET)

        time.sleep(1)

    except dropbox.exceptions.BadInputError:
        print(Fore.RED + "        The given OAuth 2 access token is malformed" + Fore.RESET)
        sys.exit(1)

    except dropbox.exceptions.AuthError as authError:

        # Checks if the error is due to an invalid token
        if authError.error.is_invalid_access_token():               # Access token has been revoked
            print(Fore.RED + "        The introduced access token does not exist or is invalid because it has been "
                             "revoked" + Fore.RESET)
            sys.exit(1)
        else:                                                       # Another error. For example: no write permission
            raise


def __create_dir(dir_name):
    """Creates a new directory named Hyot in the root path or a new subdirectory within the Hyot directory
    :param dir_name: Name of the directory or subdirectory
    """

    global dbx, path, message_dir

    # Establishes some data
    if dir_name == HYOT_DIR:
        path = "/"
        message_dir = "directory"
    else:
        path = "/Hyot/"
        message_dir = "subdirectory"

    try:

        # Creates the new directory or subdirectory
        # An error is thrown if the directory or subdirectory already exists, if there is not enough available space
        # and so on
        dbx.files_create_folder_v2(path + dir_name, autorename=False)

        print("        Creating the " + message_dir)
        print(Fore.GREEN + "        " + Style.BRIGHT + dir_name + Style.NORMAL + " " + message_dir + " was created "
                           "successfully" + Fore.RESET)

    except dropbox.exceptions.ApiError as createError:

        if createError.error.get_path().is_conflict():              # Directory or subdirectory already exists
            print(Fore.GREEN + "        " + Style.BRIGHT + dir_name + Style.NORMAL + " " + message_dir +
                  " already exists" + Fore.RESET)
            pass
        elif createError.error.get_path().is_insufficient_space():  # Insufficient space
            print("        Creating the " + message_dir)
            print(Fore.RED + "        Error to create the " + Style.BRIGHT + dir_name + Style.NORMAL +
                  " subdirectory. The user does not have enough available space (bytes) to write more data"
                  + Fore.RESET)
            sys.exit(1)
        else:                                                       # Another error. For example: no write permission
            raise


def __check_space():
    """Checks the amount of available space in the user account"""

    # Checks if there is a considerable amount of available space in the user account (at least 500MB) TODO
    allocated_space = dbx.users_get_space_usage().allocation.get_individual().allocated             # Allocated space
    used_space = dbx.users_get_space_usage().used                                                   # Used space
    available_space = allocated_space - used_space                                                  # Available space

    # Notifies the user that the space may be insufficient (< 500 MB)
    if available_space < MIN_SPACE:
        print("        " + Fore.YELLOW + "Warning!" + Fore.RESET + " The available space may be insufficient (500 MB). "
              "It is advisable to increase it before continuing the execution due to an error could occur later")

        time.sleep(2)


def init():
    """Initializes the main directory and the subdirectories by checking if these one exist or not"""

    global dht_subdir, hcsr_subdir

    # Variables
    sensor_subdirs = []                        # Defines a list with the name of the subdirectories of each sensor

    # Checks the amount of available space in the user account
    __check_space()

    # Asks the user for the subdirectory where the images of an alarm triggered by the DHT11 sensor will be stored TODO - Images?
    dht_subdir = raw_input(Fore.BLUE + "        Enter the name of the subdirectory where the images of an alarm "
                                       "triggered by the DHT11 sensor will be stored. Empty to use the default value ("
                                       + "/" + HYOT_DIR + "/" + DHT11_DIR + "): " + Fore.RESET) or DHT11_DIR

    # Asks the user for the subdirectory where the images of an alarm triggered by the HC-SR04 sensor will be stored TODO - Images?
    hcsr_subdir = raw_input(Fore.BLUE + "        Enter the name of the subdirectory where the images of an alarm "
                                        "triggered by the HC-SR04 sensor will be stored. Empty to use the default "
                                        "value (" + "/" + HYOT_DIR + "/" + HCSR04_DIR + "): "
                            + Fore.RESET) or HCSR04_DIR

    # Checks if some name is empty
    if dht_subdir.isspace() or hcsr_subdir.isspace():
        print(Fore.RED + "        The names of the sensor directories can not be empty" + Fore.RESET)
        sys.exit(1)

    # Removes spaces and converts to lowercase
    dht_subdir = dht_subdir.replace(" ", "").lower()
    hcsr_subdir = hcsr_subdir.replace(" ", "").lower()

    # Checks if both names are the same
    if dht_subdir == hcsr_subdir:
        print(Fore.RED + "        The names of the sensor directories can not be the same" + Fore.RESET)
        sys.exit(1)

    # Adds the name of each subdirectory to the list
    sensor_subdirs.append(dht_subdir)
    sensor_subdirs.append(hcsr_subdir)

    # Creates the main directory
    print("        Checking if the main directory named Hyot exists in the root path of Dropbox")
    __create_dir(HYOT_DIR)

    # Checks if each subdirectory already exists or not
    for index, sensor_subdir in enumerate(sensor_subdirs):
        print("        Checking if the subdirectory of the " + SENSORS[index] + " sensor exists within the Hyot "
              "directory in Dropbox")

        __create_dir(sensor_subdir)

        time.sleep(1)


def __get_shared_link(upload_path):
    """Creates a shared shortened link of the file. If a shared link already exists for the given path, that link is
    returned
    :param upload_path: Upload path of the current file
    :return: link Shared link of the uploaded file to Dropbox
    """

    global dbx

    try:

        link = dbx.sharing_create_shared_link(upload_path, short_url=True, pending_upload=None)
        return link.url

    except dropbox.exceptions.ApiError as sharedLinkError:

        if sharedLinkError.error.is_path():                         # File in the upload path does not exist
            print(Fore.RED + "There is no file indicated by the upload path. Please, check the way to get the shared "
                             "link" + Fore.RESET)
            sys.exit(1)
        else:                                                       # Another error
            raise


def upload_file(localfile, sensor):
    """Uploads the file to Dropbox, in particular to the subdirectory of the sensor that triggered the alarm
    :param localfile: Local path and name of the file to upload TODO
    :param sensor: Sensor that triggered the alarm
    :return: shared_link Shared link of the uploaded file to Dropbox
    """

    global dbx, dht_subdir, hcsr_subdir

    # Variables
    upload_path = None                                              # Specify upload path

    if sensor == SENSORS[0]:                                        # Upload path of the DHT11 sensor
        upload_path = "/" + HYOT_DIR + "/" + dht_subdir + "/" + "test.jpg"     # TODO

    elif sensor == SENSORS[1]:                                      # Upload path of the HC-SR04 sensor
        upload_path = "/" + HYOT_DIR + "/" + hcsr_subdir + "/" + "test.jpg"     # TODO

    try:

        print(Fore.LIGHTBLACK_EX + "  -- Uploading " + localfile + " to Dropbox like " + upload_path + Fore.RESET),
        time.sleep(1)

        # Reads the file and uploads it
        with open("/home/pi/Desktop/test.jpg", 'rb') as f:  # TODO

            # Uploads the file. An error is thrown if this one already exists,
            # if there is not enough available space and so on
            dbx.files_upload(f.read(), upload_path, autorename=False)

            # Obtains the shared link of the uploaded file to Dropbox
            shared_link = __get_shared_link(upload_path)

            print(Fore.GREEN + " ✓" + Fore.RESET)

            # Returns the shared link
            return shared_link

    except IOError:                                                        # Error to open the file

        print(Fore.RED + "Could not open the file: /home/pi/Desktop/test.jpg. No such file in the local system or "
                         "corrupt file" + Fore.RESET)  # TODO
        sys.exit(1)     # TODO

    except dropbox.exceptions.ApiError as uploadError:

        if uploadError.error.get_path().reason.is_conflict():              # Conflict with another different file TODO - Images?
            print(Fore.RED + "Existing conflict with another file with the same name and different content."
                             " Please, check the way in which the names of the images are generated" + Fore.RESET)
            sys.exit(1)
        elif uploadError.error.get_path().reason.is_insufficient_space():  # Insufficient space
            print(Fore.RED + "File not uploaded. The user does not have enough available space" + Fore.RESET)
            pass    # TODO Return None
        else:                                                      # Another error. For example: no write permission
            raise


def disconnect():
    """Disconnects the Dropbox client disabling the access token used to authenticate the calls"""

    global dbx

    if not (dbx is None):
        print("        Disconnecting the Dropbox client session"),

        time.sleep(0.25)

        try:
            # Ends the client session
            dbx = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
