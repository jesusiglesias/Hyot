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
#           FILE:     dropbox_module.py                                                                                #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic of the Dropbox service                                            #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Account in the Dropbox service, Connection to the network                                        #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     01/08/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic of the Dropbox service"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                          # System-specific parameters and functions
    import dropbox                                      # Python SDK for integrating with the Dropbox API v2
    import email_module as email                        # Module to send emails
    import time                                         # Time access and conversions
    import yaml                                         # YAML parser and emitter for Python
    from colorama import Fore, Style                    # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in dropbox_module: " + importError.message.lower() + ".")
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
HYOT_DIR = "Hyot"                       # Name of the main directory
DHT11_DIR = "dht11"                     # Name of the DHT11 sensor subdirectory
HCSR04_DIR = "hcsr04"                   # Name of the HC-SR04 sensor subdirectory
MIN_SPACE = 524288000                   # Recommended available space in the account (500 MB = 524288000 bytes)
# Names to identify the step where the error has occurred
STEP_UPLOADDROPBOX = "Upload video to Dropbox"
STEP_UPLOADDROPBOX_NOTFILE = "Upload video to Dropbox - File not found in the local system"
STEP_UPLOADDROPBOX_LINK = "Upload video to Dropbox - Get shared link"

try:
    TOKEN = conf['dropbox']['token']     # Authorization token

except (KeyError, TypeError) as keyError:
    print(Fore.RED + "✖ Please, make sure that the key: [dropbox|token] exists in the configuration file"
                     " (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
dbx = None                  # Instance of a Dropbox class
path = None                 # Path where create folders or upload files
message_dir = None          # Message
dht_subdir = None           # Final name of the DHT11 sensor subdirectory (default value or value entered by the user)
hcsr_subdir = None          # Final name of the HC-SR04 sensor subdirectory (default value or value entered by the user)
sensors = []                # Stores the name of all sensors


########################################
#               FUNCTIONS              #
########################################
def connect():
    """
    Creates an instance of the Dropbox class and establishes a connection.
    """

    global TOKEN, dbx

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Generating the client of the Dropbox service" + Style.RESET_ALL)

    # Asks the user for Dropbox token
    token = raw_input(Fore.BLUE + "        Enter the Dropbox token or empty to use the default value: "
                      + Fore.RESET) or TOKEN

    # Checks if the Dropbox token is empty
    if token.isspace():
        print(Fore.RED + "        ✖ The Dropbox token can not be empty." + Fore.RESET)
        sys.exit(0)

    # Creates an instance of the Dropbox class, which can make requests to API
    dbx = dropbox.Dropbox(token.replace(" ", ""))

    try:
        # Checks that the access token is valid
        current_user = dbx.users_get_current_account()

        print(Fore.GREEN + "        ✓ Dropbox client connected with the user: " + str(current_user.name.given_name)
              + Fore.RESET)

        time.sleep(1)

    except dropbox.exceptions.BadInputError:
        print(Fore.RED + "        ✖ The given OAuth 2 access token is malformed." + Fore.RESET)
        sys.exit(1)

    except dropbox.exceptions.AuthError as authError:

        # Checks if the error is due to an invalid token
        if authError.error.is_invalid_access_token():               # Access token has been revoked
            print(Fore.RED + "        ✖ The introduced access token does not exist or is invalid because it has been "
                             "revoked." + Fore.RESET)
            sys.exit(1)
        else:                                                       # Another error. For example: no write permission
            print(Fore.RED + "        ✖ Error to generating the client of the Dropbox service. Exception: "
                  + str(authError) + "." + Fore.RESET)
            sys.exit(1)


def __create_dir(dir_name):
    """
    Creates a new directory named Hyot in the root path or a new subdirectory within the Hyot directory.

    :param dir_name: Name of the directory or subdirectory.
    """

    global HYOT_DIR, dbx, path, message_dir

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
        print(Fore.GREEN + "        ✓ " + message_dir.title() + " was created successfully: " + dir_name + Fore.RESET)

    except dropbox.exceptions.ApiError as createError:

        if createError.error.get_path().is_conflict():              # Directory or subdirectory already exists
            print(Fore.GREEN + "        ✓ " + Fore.CYAN + message_dir.title() + " already exists" + Fore.RESET)

        elif createError.error.get_path().is_insufficient_space():  # Insufficient space
            print("        Creating the " + message_dir)
            print(Fore.RED + "        ✖ Error to create the subdirectory: " + dir_name + ". The user does not have"
                             " enough available space (bytes) to write more data." + Fore.RESET)
            sys.exit(1)
        else:                                                       # Another error. For example: no write permission
            print(Fore.RED + "        ✖ Error to create the directory o subdirectory. Exception: " + str(createError)
                  + "." + Fore.RESET)
            sys.exit(1)


def __check_space():
    """
    Checks the amount of available space in the user account.
    """

    global MIN_SPACE, dbx

    # Checks if there is a considerable amount of available space in the user account (at least 500MB)
    allocated_space = dbx.users_get_space_usage().allocation.get_individual().allocated             # Allocated space
    used_space = dbx.users_get_space_usage().used                                                   # Used space
    available_space = allocated_space - used_space                                                  # Available space

    # Notifies the user that the space may be insufficient (< 500 MB)
    if available_space < MIN_SPACE:
        print(Fore.YELLOW + "        Warning!" + Fore.RESET + " The available space may be insufficient (500 MB). "
              "It is advisable to increase it before continuing the execution due to an error could occur later.")

        time.sleep(2)


def init(all_sensors):
    """
    Initializes the main directory and the subdirectories by checking if these one exist or not.

    :param all_sensors: Name of the sensors.
    """

    global DHT11_DIR, HCSR04_DIR, HYOT_DIR, dht_subdir, hcsr_subdir, sensors

    # Variables
    sensor_subdirs = []                        # Defines a list with the name of the subdirectories of each sensor
    sensors = all_sensors                      # Name of all sensors

    # Checks the amount of available space in the user account
    __check_space()

    # Asks the user for the subdirectory where the videos of an alarm triggered by the DHT11 sensor will be stored
    dht_subdir = raw_input(Fore.BLUE + "        Enter the name of the subdirectory where the videos of an alarm "
                                       "triggered by the DHT11 sensor will be stored: " + Fore.WHITE + "(" + "/"
                           + HYOT_DIR + "/" + DHT11_DIR + ") " + Fore.RESET) or DHT11_DIR

    # Asks the user for the subdirectory where the videos of an alarm triggered by the HC-SR04 sensor will be stored
    hcsr_subdir = raw_input(Fore.BLUE + "        Enter the name of the subdirectory where the videos of an alarm "
                                        "triggered by the HC-SR04 sensor will be stored: " + Fore.WHITE + "(" + "/"
                            + HYOT_DIR + "/" + HCSR04_DIR + ") " + Fore.RESET) or HCSR04_DIR

    # Checks if some name is empty
    if dht_subdir.isspace() or hcsr_subdir.isspace():
        print(Fore.RED + "        ✖ The names of the sensor directories can not be empty." + Fore.RESET)
        sys.exit(0)

    # Removes spaces and converts to lowercase
    dht_subdir = dht_subdir.replace(" ", "").lower()
    hcsr_subdir = hcsr_subdir.replace(" ", "").lower()

    # Checks if both names are the same
    if dht_subdir == hcsr_subdir:
        print(Fore.RED + "        ✖ The names of the sensor directories can not be the same." + Fore.RESET)
        sys.exit(0)

    # Adds the name of each subdirectory to the list
    sensor_subdirs.append(dht_subdir)
    sensor_subdirs.append(hcsr_subdir)

    print("        Checking if the main directory named Hyot exists in the root path of Dropbox")

    # Creates the main directory
    __create_dir(HYOT_DIR)

    # Checks if each subdirectory already exists or not
    for index, sensor_subdir in enumerate(sensor_subdirs):
        print("        Checking if the subdirectory of the " + sensors[index] + " sensor exists within the Hyot "
              "directory in Dropbox")

        __create_dir(sensor_subdir)

        time.sleep(1)

    time.sleep(1)
    print("\n        ------------------------------------------------------")


def __get_shared_link(upload_path, mailto):
    """
    Creates a shared shortened link of the file. If a shared link already exists for the given path, that link is
    returned.

    :param upload_path: Upload path of the current file.
    :param mailto: Email address where to send the error notification if it occurs.

    :return: link Link of the uploaded file to Dropbox.
    """

    global STEP_UPLOADDROPBOX_LINK, dbx

    try:
        link = dbx.sharing_create_shared_link(upload_path, short_url=True, pending_upload=None)
        return link.url

    except dropbox.exceptions.ApiError as sharedLinkError:

        if sharedLinkError.error.is_path():                         # File in the upload path does not exist
            print(Fore.RED + " ✖ There is no file indicated by the upload path. Please, check the way to get the"
                             " shared link.\n" + Fore.RESET)
        else:                                                       # Another error
            print(Fore.RED + " ✖ Error to create the shared link of the file in Dropbox. Exception: "
                  + str(sharedLinkError) + ".\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        email.print_error_notification_or_send_email(mailto, STEP_UPLOADDROPBOX_LINK)

        sys.exit(1)


def upload_file(localfile, sensor, mailto):
    """
    Uploads the file to the Cloud (Dropbox), in particular to the subdirectory of the sensor that triggered the alarm.

    :param localfile: Local path and name of the file to upload.
    :param sensor: Sensor that triggered the alarm.
    :param mailto: Email address where to send the error notification if it occurs.

    :return: link Link of the uploaded file to Dropbox.
    """

    global HYOT_DIR, STEP_UPLOADDROPBOX_NOTFILE, STEP_UPLOADDROPBOX, dbx, dht_subdir, hcsr_subdir

    # Variables
    upload_path = None                                              # Specify upload path
    name = str(localfile.split("/")[-1])                            # Name of the file to upload

    if sensor == sensors[0]:                                        # Upload path of the DHT11 sensor
        upload_path = "/" + HYOT_DIR + "/" + dht_subdir + "/" + name

    elif sensor == sensors[1]:                                      # Upload path of the HC-SR04 sensor
        upload_path = "/" + HYOT_DIR + "/" + hcsr_subdir + "/" + name

    try:
        print(Fore.LIGHTBLACK_EX + "     -- Uploading the recording to Dropbox to the path: " + upload_path
              + Fore.RESET),
        time.sleep(0.5)

        # Reads the file and uploads it
        with open(localfile, 'rb') as f:

            # Uploads the file. An error is thrown if this one already exists,
            # if there is not enough available space and so on
            dbx.files_upload(f.read(), upload_path, autorename=False)

            # Obtains the link of the uploaded file to Dropbox
            link = __get_shared_link(upload_path, mailto)

            print(Fore.GREEN + " ✓" + Fore.RESET)

            # Returns the link
            return link

    except IOError:                                                        # Error to open the file

        print(Fore.RED + "✖ Could not open the file: " + localfile + ". No such file in the local system or corrupt"
                         " file.\n")

        # Prints a message or sends an email when an error occurs during the alert protocol
        email.print_error_notification_or_send_email(mailto, STEP_UPLOADDROPBOX_NOTFILE)

        sys.exit(1)

    except dropbox.exceptions.ApiError as uploadError:

        if uploadError.error.get_path().reason.is_conflict():              # Conflict with another different file
            print(Fore.RED + " ✖ Existing conflict with another file with the same name and different content."
                             " Please, check the way in which the names of the videos are generated.\n" + Fore.RESET)

        elif uploadError.error.get_path().reason.is_insufficient_space():  # Insufficient space
            print(Fore.RED + " ✖ File not uploaded. The user does not have enough available space.\n" + Fore.RESET)

        else:                                                      # Another error. For example: no write permission
            print(Fore.RED + " ✖ Error to upload the recording to Dropbox. Exception: " + str(uploadError) + ".\n"
                  + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        email.print_error_notification_or_send_email(mailto, STEP_UPLOADDROPBOX)

        sys.exit(1)


def disconnect():
    """
    Disconnects the Dropbox client disabling the access token used to authenticate the requests.
    """

    global dbx

    if not (dbx is None):
        print("      Disconnecting the Dropbox client session"),

        time.sleep(0.25)

        try:
            # Ends the client session
            dbx = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
