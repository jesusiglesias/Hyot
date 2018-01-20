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
#           FILE:     cloudantdb_module.py                                                                             #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic of the Cloudant NoSQL database (IBM Cloud service)                #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Account in the Cloudant NoSQL database service                                                   #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/05/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic of the Cloudant NoSQL database (IBM Cloud service)"""

########################################
#               IMPORTS                #
########################################

try:
    import sys                                      # System-specific parameters and functions
    import time                                     # Time access and conversions
    from colorama import Fore, Style                # Cross-platform colored terminal text
    from cloudant.client import Cloudant            # Cloudant NoSQL DB client

except ImportError as importError:
    print("Error to import: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
SENSORS = ["DHT11", "HC-SR04"]                                                    # Name of the sensors
USERNAME_DB = "ee585910-3df5-46f4-93a6-85400da6734e-bluemix"                      # User name in Cloudant NoSQL DB
PASSWORD_DB = "2d612e9875d92b3a6fd14b8a763ffb05f23bde3a81d9298f2e372245508ce25c"  # Password in Cloudant NoSQL DB
URL_DB = "https://ee585910-3df5-46f4-93a6-85400da6734e-bluemix:2d612e9875d92b3a" \
         "6fd14b8a763ffb05f23bde3a81d9298f2e372245508ce25c@ee585910-3df5-46f4-9" \
         "3a6-85400da6734e-bluemix.cloudant.com"                                  # URL in Cloudant NoSQL DB
DHT11_DB = "dht11_measurements"                                                   # Name of the DHT11 sensor database
HCSR04_DB = "hcsr04_measurements"                                                 # Name of the HC-SR04 sensor database


########################################
#           GLOBAL VARIABLES           #
########################################
client = None                                                                     # Cloudant NoSQL DB client
dbs_instances = None                                                              # Instances of all databases


########################################
#               FUNCTIONS              #
########################################
def connect():
    """Creates a Cloudant DB client and establishes a connection"""

    global client

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Generating the client of the Cloudant NoSQL DB service"
          + Style.RESET_ALL)

    # Asks the user for Cloudant credentials
    username = raw_input(Fore.BLUE + "        Enter the Cloudant username or empty to use the default value: "
                         + Fore.RESET) or USERNAME_DB
    password = raw_input(Fore.BLUE + "        Enter the Cloudant password or empty to use the default value: "
                         + Fore.RESET) or PASSWORD_DB
    url = raw_input(Fore.BLUE + "        Enter the Cloudant URL or empty to use the default value: "
                    + Fore.RESET) or URL_DB

    # Checks if some Cloudant DB credential is empty
    if username.isspace() or password.isspace() or url.isspace():
        print(Fore.RED + "        The Cloudant DB credentials can not be empty" + Fore.RESET)
        sys.exit(1)

    # Creates the client using auto_renew to automatically renew expired cookie auth
    client = Cloudant(username.replace(" ", ""), password.replace(" ", ""), url=url.replace(" ", ""),
                      connect=True, auto_renew=True)

    # Establishes a connection with the service instance
    client.connect()

    print(Fore.GREEN + "        Cloudant DB client connected" + Fore.RESET)

    time.sleep(1)


def init(timestamp):
    """Initializes the DB by checking if these one exist or not
    :param timestamp: Datetime when the measurement was taken
    """

    global client, dbs_instances

    dht11_dbinstance = None                                # Instance for the DHT11 sensor database
    hcsr04_dbinstance = None                               # Instance for the HC-SR04 sensor database
    dbs_instances = [dht11_dbinstance, hcsr04_dbinstance]  # Defines a list with the instances of the databases
    sensor_dbs = []                                        # Defines a list with the name of the database of each sensor

    # Asks the user for the name of the DHT11 sensor database
    dht_database = raw_input(Fore.BLUE + "        Enter the name for the DHT11 sensor database. Empty to use the "
                                         "default value (" + DHT11_DB + "(_timestamp)): " + Fore.RESET) or DHT11_DB

    # Asks the user for the name of the HC-SR04 sensor database
    hcsr_database = raw_input(Fore.BLUE + "        Enter the name for the HC-SR04 sensor database. Empty to use the "
                                          "default value (" + HCSR04_DB + "(_timestamp)): " + Fore.RESET) or HCSR04_DB

    # Checks if some name is empty
    if dht_database.isspace() or hcsr_database.isspace():
        print(Fore.RED + "        The names of the sensor databases can not be empty" + Fore.RESET)
        sys.exit(1)

    # Removes spaces and converts to lowercase
    dht_database = dht_database.replace(" ", "").lower()
    hcsr_database = hcsr_database.replace(" ", "").lower()

    # Checks if both names are the same
    if dht_database == hcsr_database:
        print(Fore.RED + "        The names of the sensor databases can not be the same" + Fore.RESET)
        sys.exit(1)

    # Adds the name of each database to the list where the name includes the current month and year
    sensor_dbs.append(dht_database + "_" + str(timestamp.strftime("%Y-%m")))
    sensor_dbs.append(hcsr_database + "_" + str(timestamp.strftime("%Y-%m")))

    # Retrieves the list of all database names for the current client
    all_databases = client.all_dbs()

    # Loops in each database to use
    for index, db in enumerate(sensor_dbs):
        print("        Checking if the database of the " + SENSORS[index] + " sensor exists in the Cloudant NoSQL "
              "DB service")

        # Checks if the database exists in the Cloudant NoSQL DB service
        if db in all_databases:

            # Opens the existing database of the DHT11 sensor
            dbs_instances[index] = client[db]

            print(Fore.GREEN + "        " + Style.BRIGHT + db + Style.NORMAL + " database already exists and was "
                               "opened successfully" + Fore.RESET)
        else:
            print("        Initializing the database")

            # Creates the database using the initialized client. The result is a new CloudantDatabase instance
            # based on the client
            dbs_instances[index] = client.create_database(db)

            # Checks that the database was created successfully
            if dbs_instances[index].exists():
                print(Fore.GREEN + "        " + Style.BRIGHT + db + Style.NORMAL + " database was created successfully"
                      + Fore.RESET)
            else:
                print(Fore.RED + "        Error to create the " + Style.BRIGHT + db + Style.NORMAL + " database. "
                                 "Please, check the Cloudant NoSQL DB service" + Fore.RESET)
                sys.exit(1)

        time.sleep(1)

    print("\n        ------------------------------------------------------")


def add_document(data, sensor):
    """Adds a new document to the database and checks later that the document exists
    :param data: Document to save in the database
    :param sensor: Sensor type
    """

    global dbs_instances

    db_instance = None                                      # Instance of a specific database

    # Selects the database instance based on sensor type
    if sensor == SENSORS[0]:                                # DHT11 sensor
        db_instance = dbs_instances[0]
    elif sensor == SENSORS[1]:                              # HC-SR04 sensor
        db_instance = dbs_instances[1]

    # Creates a document using the Database API
    document = db_instance.create_document(data, throw_on_exists=True)

    # Checks that the document exists in the database
    if document.exists():
        print(Fore.GREEN + "Measurement added to database successfully" + Fore.RESET)
    else:
        print(Fore.RED + "Error to add the measurement. Please, check the Cloudant NoSQL DB service" + Fore.RESET)
        sys.exit(1)


def disconnect():
    """Disconnects the Cloudant client"""

    global client

    if not (client is None):
        print("        Disconnecting the Cloudant DB client")

        # Ends the client session
        client.disconnect()

        print(Fore.GREEN + "        Cloudant DB session ends successfully" + Fore.RESET)
