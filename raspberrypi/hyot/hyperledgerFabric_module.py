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
#           FILE:     hyperledgerFabric_module.py                                                                      #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to interact with the blockchain of Hyperledger Fabric             #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     TODO                                                                                             #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     02/18/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic to interact with the blockchain of Hyperledger Fabric"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import time                                     # Time access and conversions
    import hashlib                                  # Secure hashes and message digests
    import json                                     # JSON encoder and decoder
    import re                                       # Regular expression
    import requests                                 # HTTP for Humans
    import sha3                                     # SHA-3 wrapper (Keccak) for Python
    import socket                                   # Low-level networking interface
    import yaml                                     # YAML parser and emitter for Python
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in hyperledgerFabric_module: " + importError.message.lower() + ".")
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
BLOCKSIZE = 65536                                       # Block size (64kb) to hash
HLC_HOST = conf['hl']['host']                           # Default host where Hyperledger Composer REST server is running
HLC_PORT = conf['hl']['port']                           # Default port where Hyperledger Composer REST server is running


########################################
#           GLOBAL VARIABLES           #
########################################
hlc_server_host = None                                  # Host where Hyperledger Composer REST server is running
hlc_server_port = None                                  # Port where Hyperledger Composer REST server is running
hlc_server_url = None                                   # Full address where Hyperledger Composer REST server is running
key_participant = "participant"                         # Key to search in a JSON format file
value_participant = "org.hyperledger.composer.system"   # Value that the 'participant key must contain


########################################
#               FUNCTIONS              #
########################################
def __is_jsonable(response):
    """Checks if the response is a JSON serializable and contains the 'participant' key
    :param response: Response of the request
    :return: True, if the response is a JSON serializable and contains the specified key. False, otherwise
    """

    global key_participant

    try:
        # Serializes the response in JSON format
        response_json = response.json()

        # Checks if the key exists
        if key_participant in response_json:
            return True
        else:
            return False
    except ValueError:
        return False


def __hlc_ping():
    """Checks if the address belongs to a business network of Hyperledger Fabric through running a ping with REST API
     exposed by the Hyperledger Composer REST server
    :return: True, if the address belongs to a business network. False, otherwise
    """

    global hlc_server_url, key_participant, value_participant

    # Headers of the GET request
    headers = {
        "Accept": "application/json",
    }

    print("        Pinging the business network of the address: " + hlc_server_url)

    # GET request - Ping
    response = requests.get(hlc_server_url + "/api/system/ping", headers=headers)

    # Checks if the response is a JSON serializable and contains a specified key
    if __is_jsonable(response):

        # Response is OK (200) and the 'participant' key contains a regular expression
        if response.status_code == requests.codes.ok and re.match(r"%s" % value_participant,
                                                                  response.json()[key_participant]):

            print(Fore.GREEN + "        Business network is alive in the address" + Fore.RESET)

        else:
            if "error" in (response.json()):
                print(Fore.RED + "        Wrong request. Error: " + str(response.status_code) + ". " +
                      str(response.json()['error']['name']) + ": " + str(response.json()['error']['message']) +
                      Fore.RESET)
            else:
                print(Fore.RED + "        Participant key in the response does not contain the following regular"
                                 " expression: " + value_participant + ". " + Fore.RESET)
            sys.exit(0)

    else:
        print(Fore.RED + "        Response of Ping request is not a JSON serializable or it does not contain the"
                         " 'participant' key" + Fore.RESET)
        sys.exit(0)


def __port_isdigit(port):
    """Checks if the given port is a number
    :param port: Port of the address
    :return: True if the string only contains digits. False, otherwise
    """
    return port.replace(".", "", 1).isdigit()


def init():
    """Checks if Hyperledger Fabric is alive through running a ping with REST API exposed by the Hyperledger Composer
    REST server. This REST server allows to interact with the business network deployed in the blockchain of Hyperledger
    Fabric"""

    global HLC_HOST, HLC_PORT, hlc_server_host, hlc_server_port, hlc_server_url

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Checking if the business network in Hyperledger Fabric is alive"
          + Style.RESET_ALL)

    # Asks the user for the host where Hyperledger Composer REST server is running
    hlc_server_host = raw_input(Fore.BLUE + "        Enter the host where Hyperledger Composer REST server is "
                                            "running: " + Fore.WHITE + "(" + HLC_HOST + ") " + Fore.RESET) or HLC_HOST

    # Checks if the host is empty
    if hlc_server_host.isspace():
        print(Fore.RED + "        The host of the Hyperledger Composer REST server can not be empty" + Fore.RESET)
        sys.exit(0)

    # Removes the substrings
    hlc_server_host = hlc_server_host.replace("http://", "").replace("https://", "")

    # Asks the user for the port where Hyperledger Composer REST server is running
    hlc_server_port = raw_input(Fore.BLUE + "        Enter the port where Hyperledger Composer REST server is running: "
                                + Fore.WHITE + "(" + str(HLC_PORT) + ") " + Fore.RESET) or HLC_PORT

    # Checks if the port is empty
    if str(hlc_server_port).isspace():
        print(Fore.RED + "        The port of the Hyperledger Composer REST server can not be empty" + Fore.RESET)
        sys.exit(0)

    # Checks if the port is a number
    if not __port_isdigit(str(hlc_server_port)):
        print(Fore.RED + "        The port of the Hyperledger Composer REST server can only be a number" + Fore.RESET)
        sys.exit(0)

    # Full address
    hlc_server_url = "http://" + hlc_server_host + ":" + str(hlc_server_port)

    # Checks if this host and port is alive and listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Creates an INET socket of type STREAM
    sock.settimeout(2)                                             # Set a timeout (2 sec) on blocking socket operations

    try:
        print("        Checking if this host and port is alive and listen")

        # Connects to a remote socket at address
        result_connection = sock.connect_ex((hlc_server_host, int(hlc_server_port)))

        # Host and port is running and alive
        if result_connection == 0:
            print(Fore.GREEN + "        Port " + str(hlc_server_port) + " in " + hlc_server_host + " reachable"
                  + Fore.RESET)

            # Checks if this address belongs to Hyperledger Composer REST server
            __hlc_ping()
        else:
            print(Fore.RED + "        Connection closed in this address. Error on connect: " + str(result_connection)
                  + Fore.RESET)
            sys.exit(0)
    except socket.gaierror:
        print(Fore.RED + "        Given host is invalid" + Fore.RESET)
        sys.exit(0)
    finally:
        sock.close()                                               # Closes the socket


def publishAlert_transaction(uuid, timestamp, alert_origin, hash_video, shared_link):
    """Submits a transaction to publish a new alert asset in the blockchain of Hyperledger Fabric
    :param uuid: Identifier of the alert
    :param timestamp: Datetime of the alert
    :param alert_origin: Indicates the sensor that triggered the alert
    :param hash_video: Hash of the content of the video
    :param shared_link: Link to Dropbox where the file was uploaded
    """

    global hlc_server_url

    # Headers of the POST request
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Properties of the transaction in JSON format
    payload = {
        "$class": 'org.hyot.network.PublishAlert',
        "alert_id": uuid,
        "alert_details": {
            "$class": 'org.hyot.network.AlertDetails',
            "timestamp": str(timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            "alert_origin": alert_origin,
            "hash": hash_video,
            "shared_link": shared_link,
            "owner": 'resource:org.hyot.network.User#jesusiglesias',
        }
    }

    print(Fore.LIGHTBLACK_EX + "   -- Submitting the transaction to publish the alert to the blockchain of Hyperledger"
                               " Fabric" + Fore.RESET),
    time.sleep(0.5)

    # POST request - PublishAlert transaction
    response = requests.post(hlc_server_url + '/api/PublishAlert', headers=headers, data=json.dumps(payload))

    # Request is OK (200)
    if response.status_code == requests.codes.ok:
        print(Fore.GREEN + " ✓" + Fore.RESET)
    else:
        print(Fore.RED + " ✕ Error to submit the transaction (code " + str(response.status_code) + "). "
              + str(response.json()['error']['message']) + Fore.RESET)
        sys.exit(0)


def file_hash(video):
    """Applies a hash function to the content of the file
    :param video: File to hash
    :return: Hash of the video file
    """

    global BLOCKSIZE

    try:
        print(Fore.LIGHTBLACK_EX + "   -- Applying a hash function to the content of the video" + Fore.RESET),

        time.sleep(1)

        # Variables
        hasher = hashlib.sha3_512()

        # Opens the file in read and binary mode
        with open(video, 'rb', buffering=0) as f:

            # Reads chunks of a certain size (64kb) to avoid memory failures when not knowing the size of the file
            for b in iter(lambda: f.read(BLOCKSIZE), b''):
                hasher.update(b)                                   # Updates the hash

        print(Fore.GREEN + " ✓" + Fore.RESET)

        # Hash
        return hasher.hexdigest()

    except Exception as hashError:

        print(Fore.RED + " ✕ Error to apply the hash function to the video: " + str(hashError) + Fore.RESET)
        sys.exit(1)  # TODO
