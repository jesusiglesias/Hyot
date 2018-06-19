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
#           FILE:     cloudantdb_module.py                                                                             #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic of the Cloudant NoSQL database (IBM Cloud service)                #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Account in the Cloudant NoSQL database service, Connection to the network                        #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     01/05/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic of the Cloudant NoSQL database (IBM Cloud service)"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import getpass                                  # Portable password input
    import time                                     # Time access and conversions
    import yaml                                     # YAML parser and emitter for Python
    from cloudant.client import Cloudant            # Cloudant NoSQL DB client
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in cloudantdb_module: " + importError.message.lower() + ".")
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
    USERNAME_DB = conf['cloudant']['username']      # User name in Cloudant NoSQL DB
    PASSWORD_DB = conf['cloudant']['password']      # Password in Cloudant NoSQL DB
    URL_DB = conf['cloudant']['url']                # URL in Cloudant NoSQL DB

except (KeyError, TypeError) as keyError:
    print(Fore.RED + "✖ Please, make sure that the keys: [cloudant|username], [cloudant|password] and [cloudant|url] "
                     "exist in the configuration file (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)

SENSOR_DB = "sensors_measurements"                  # Name of the database that will stores the values of the sensors


########################################
#           GLOBAL VARIABLES           #
########################################
client = None                                       # Cloudant NoSQL DB client
db_instance = None                                  # Instance of the database
db_name = None                                      # Name of the database


########################################
#               FUNCTIONS              #
########################################
def connect():
    """
    Creates a Cloudant DB client and establishes a connection.
    """

    global USERNAME_DB, PASSWORD_DB, URL_DB, client

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Generating the client of the Cloudant NoSQL DB service"
          + Style.RESET_ALL)

    # Asks the user for Cloudant credentials
    username = raw_input(Fore.BLUE + "        Enter the Cloudant username or empty to use the default value: "
                         + Fore.RESET) or USERNAME_DB
    password = getpass.getpass(Fore.BLUE + "        Enter the Cloudant password or empty to use the default value: "
                               + Fore.RESET) or PASSWORD_DB
    url = raw_input(Fore.BLUE + "        Enter the Cloudant URL or empty to use the default value: "
                    + Fore.RESET) or URL_DB

    # Checks if some Cloudant DB credential is empty
    if username.isspace() or password.isspace() or url.isspace():
        print(Fore.RED + "        ✖ The Cloudant DB credentials can not be empty." + Fore.RESET)
        sys.exit(0)

    try:
        # Creates the client using auto_renew to automatically renew expired cookie auth
        client = Cloudant(username.replace(" ", ""), password.replace(" ", ""), url=url.replace(" ", ""),
                          connect=True, auto_renew=True)

        # Establishes a connection with the service instance
        client.connect()

        print(Fore.GREEN + "        ✓ Cloudant DB client connected" + Fore.RESET)

    except Exception as cloudantError:
        print(Fore.RED + "        ✖ Error to initialize the Cloudant DB client. Exception: " + str(cloudantError) + "."
              + Fore.RESET)
        sys.exit(1)

    time.sleep(1)


def init(timestamp):
    """
    Initializes the DB by checking if these one exist or not.

    :param timestamp: Datetime when the measurement was taken.
    """

    global SENSOR_DB, client, db_name, db_instance

    db_instance = None                              # Instance for the database

    # Asks the user for the name of the database of the sensors
    db_name = raw_input(Fore.BLUE + "        Enter the name for the database of the sensors: " + Fore.WHITE + "("
                        + SENSOR_DB + "_timestamp) " + Fore.RESET) or SENSOR_DB

    # Checks if the name is empty
    if db_name.isspace():
        print(Fore.RED + "        ✖ The name of the database can not be empty." + Fore.RESET)
        sys.exit(0)

    # Removes the spaces and converts to lowercase
    db_name = db_name.replace(" ", "").lower()

    # Adds the current month and year to the name of the database
    db_name = db_name + "_" + str(timestamp.strftime("%Y-%m"))

    # Retrieves the list of all database names for the current client
    all_databases = client.all_dbs()

    print("        Checking if the database already exists in the Cloudant NoSQL DB service")

    # Checks if the database exists in the Cloudant NoSQL DB service
    if db_name in all_databases:

        # Opens the existing database
        db_instance = client[db_name]

        print(Fore.GREEN + "        ✓" + Fore.CYAN + " Database already exists and was opened successfully"
              + Fore.RESET)
    else:
        print("        Initializing the database")

        # Creates the database using the initialized client. The result is a new CloudantDatabase instance based on
        # the client
        db_instance = client.create_database(db_name)

        # Checks that the database was created successfully
        if db_instance.exists():
            print(Fore.GREEN + "        ✓ Database was created successfully" + Fore.RESET)
        else:
            print(Fore.RED + "        ✖ Error to create the database. Please, check the Cloudant NoSQL DB service."
                  + Fore.RESET)
            sys.exit(0)

    time.sleep(1)

    print("\n        ------------------------------------------------------")


def add_document(data):
    """
    Adds a new document to the database and checks later that the document exists.

    :param data: Document to save in the database.
    """

    global db_instance, db_name

    print(Fore.LIGHTBLACK_EX + "     -- Adding the measurement to the database: " + db_name + Fore.RESET),
    time.sleep(0.5)

    # Creates a document using the Database API
    document = db_instance.create_document(data, throw_on_exists=True)

    # Checks that the document exists in the database
    if document.exists():
        print(Fore.GREEN + " ✓" + Fore.RESET)
    else:
        print(Fore.RED + " ✖ Error to add the measurement. Please, check the Cloudant NoSQL DB service." + Fore.RESET)
        sys.exit(0)  # TODO Logger


def disconnect():
    """
    Disconnects the Cloudant client.
    """

    global client

    if not (client is None):
        print("      Disconnecting the Cloudant DB client session"),

        time.sleep(0.25)

        try:
            # Ends the client session
            client.disconnect()
            client = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✖" + Fore.RESET)
            raise

        time.sleep(0.25)
