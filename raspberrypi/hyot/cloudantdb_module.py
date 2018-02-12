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
#        CREATED:     01/05/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic of the Cloudant NoSQL database (IBM Cloud service)"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import time                                     # Time access and conversions
    import getpass                                  # Portable password input
    import yaml                                     # YAML parser and emitter for Python
    from colorama import Fore, Style                # Cross-platform colored terminal text
    from cloudant.client import Cloudant            # Cloudant NoSQL DB client

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
    USERNAME_DB = conf['cloudant']['username']      # User name in Cloudant NoSQL DB
    PASSWORD_DB = conf['cloudant']['password']      # Password in Cloudant NoSQL DB
    URL_DB = conf['cloudant']['url']                # URL in Cloudant NoSQL DB
except (KeyError, TypeError) as keyError:
    print(Fore.RED + "Please, make sure that the keys: [cloudant|username], [cloudant|password] and [cloudant|url] "
                     "exist in the configuration file (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)

DHT11_DB = "dht11_measurements"                     # Name of the DHT11 sensor database
HCSR04_DB = "hcsr04_measurements"                   # Name of the HC-SR04 sensor database


########################################
#           GLOBAL VARIABLES           #
########################################
client = None                                       # Cloudant NoSQL DB client
dbs_instances = None                                # Instances of all databases
sensors = []                                        # Stores the name of all sensors


########################################
#               FUNCTIONS              #
########################################
def connect():
    """Creates a Cloudant DB client and establishes a connection"""

    global client, USERNAME_DB, PASSWORD_DB, URL_DB

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
        print(Fore.RED + "        The Cloudant DB credentials can not be empty" + Fore.RESET)
        sys.exit(0)

    # Creates the client using auto_renew to automatically renew expired cookie auth
    client = Cloudant(username.replace(" ", ""), password.replace(" ", ""), url=url.replace(" ", ""),
                      connect=True, auto_renew=True)

    # Establishes a connection with the service instance
    client.connect()

    print(Fore.GREEN + "        Cloudant DB client connected" + Fore.RESET)

    time.sleep(1)


def init(timestamp, all_sensors):
    """Initializes the DB by checking if these one exist or not
    :param timestamp: Datetime when the measurement was taken
    :param all_sensors: Name of the sensors
    """

    global client, dbs_instances, sensor_dbs, sensors, DHT11_DB, HCSR04_DB

    dht11_dbinstance = None                                # Instance for the DHT11 sensor database
    hcsr04_dbinstance = None                               # Instance for the HC-SR04 sensor database
    dbs_instances = [dht11_dbinstance, hcsr04_dbinstance]  # Defines a list with the instances of the databases
    sensor_dbs = []                                        # Defines a list with the name of the database of each sensor
    sensors = all_sensors                                  # Name of all sensors

    # Asks the user for the name of the DHT11 sensor database
    dht_database = raw_input(Fore.BLUE + "        Enter the name for the DHT11 sensor database. Empty to use the "
                                         "default value (" + DHT11_DB + "(_timestamp)): " + Fore.RESET) or DHT11_DB

    # Asks the user for the name of the HC-SR04 sensor database
    hcsr_database = raw_input(Fore.BLUE + "        Enter the name for the HC-SR04 sensor database. Empty to use the "
                                          "default value (" + HCSR04_DB + "(_timestamp)): " + Fore.RESET) or HCSR04_DB

    # Checks if some name is empty
    if dht_database.isspace() or hcsr_database.isspace():
        print(Fore.RED + "        The names of the sensor databases can not be empty" + Fore.RESET)
        sys.exit(0)

    # Removes spaces and converts to lowercase
    dht_database = dht_database.replace(" ", "").lower()
    hcsr_database = hcsr_database.replace(" ", "").lower()

    # Checks if both names are the same
    if dht_database == hcsr_database:
        print(Fore.RED + "        The names of the sensor databases can not be the same" + Fore.RESET)
        sys.exit(0)

    # Adds the name of each database to the list where the name includes the current month and year
    sensor_dbs.append(dht_database + "_" + str(timestamp.strftime("%Y-%m")))
    sensor_dbs.append(hcsr_database + "_" + str(timestamp.strftime("%Y-%m")))

    # Retrieves the list of all database names for the current client
    all_databases = client.all_dbs()

    # Loops in each database to use
    for index, db in enumerate(sensor_dbs):
        print("        Checking if the database of the " + sensors[index] + " sensor exists in the Cloudant NoSQL "
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
                sys.exit(0)

        time.sleep(1)

    print("\n        ------------------------------------------------------")


def add_document(data, sensor):
    """Adds a new document to the database and checks later that the document exists
    :param data: Document to save in the database
    :param sensor: Sensor type
    """

    global dbs_instances, sensor_dbs

    db_instance = None                                      # Instance of a specific database
    db_name = None                                          # Name of the database

    # Selects the database instance based on sensor type
    if sensor == sensors[0]:                                # DHT11 sensor
        db_instance = dbs_instances[0]
        db_name = sensor_dbs[0]
    elif sensor == sensors[1]:                              # HC-SR04 sensor
        db_instance = dbs_instances[1]
        db_name = sensor_dbs[1]

    print(Fore.LIGHTBLACK_EX + "   -- Adding the measurement to the database: " + db_name + Fore.RESET),
    time.sleep(0.5)

    # Creates a document using the Database API
    document = db_instance.create_document(data, throw_on_exists=True)

    # Checks that the document exists in the database
    if document.exists():
        print(Fore.GREEN + " ✓" + Fore.RESET)
    else:
        print(Fore.RED + " ✕ Error to add the measurement. Please, check the Cloudant NoSQL DB service" + Fore.RESET)
        sys.exit(0)


def disconnect():
    """Disconnects the Cloudant client"""

    global client

    if not (client is None):
        print("        Disconnecting the Cloudant DB client session"),

        time.sleep(0.25)

        try:
            # Ends the client session
            client.disconnect()
            client = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
