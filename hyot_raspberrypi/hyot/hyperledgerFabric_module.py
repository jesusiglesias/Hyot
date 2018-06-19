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
#           FILE:     hyperledgerFabric_module.py                                                                      #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to interact with the Blockchain of Hyperledger Fabric             #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Business network deployed in Hyperledger Fabric, Hyperledger Composer REST server running,       #
#                     Connection to the network                                                                        #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     01/18/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic to interact with the Blockchain of Hyperledger Fabric"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import hashlib                                  # Secure hashes and message digests
    import json                                     # JSON encoder and decoder
    import re                                       # Regular expression
    import requests                                 # HTTP for Humans
    import sha3                                     # SHA-3 wrapper (Keccak) for Python
    import socket                                   # Low-level networking interface
    import time                                     # Time access and conversions
    import token_module as token                    # Module that contains the logic for generating secure tokens
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
    print(Fore.RED + "✖ Please, place the configuration file (hyot.yml) inside a directory called 'conf' in the root "
                     "path (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)
except yaml.YAMLError as yamlError:
    print(Fore.RED + "The configuration file (conf/hyot.yml) has not the YAML format." + Fore.RESET)
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
BLOCKSIZE = 65536                                       # Block size (64kb) to hash
HTTP = "http://"                                        # HTTP protocol in the URL
HTTPS = "https://"                                      # HTTPS protocol in the URL
HTTP_PORT = 80                                          # Default HTTP port
HTTPS_PORT = 443                                        # Default HTTPS port
HLC_HOST = conf['hl']['host']                           # Default host where Hyperledger Composer REST server is running
HLC_PORT = conf['hl']['port']                           # Default port where Hyperledger Composer REST server is running
HLC_API_PING = "/api/system/ping"                       # Hyperledger Composer REST server API - Ping
# Hyperledger Composer REST server API - Publish alert transaction
HLC_API_PUBLISH_ALERT = "/api/org.hyot.network.PublishAlert"
KEY_PARTICIPANT = "participant"                         # Key to search in a JSON format file
# Regex of the possible values that the 'participant key should contain
REGEX_VALUE_PARTICIPANT_USER = "^org\.hyot\.network\.User\#\w+$"
REGEX_VALUE_PARTICIPANT_NETWORKADMIN = "^org\.hyperledger\.composer\.system\.NetworkAdmin\#\w+$"
# Possible values that the 'participant key should contain
VALUE_PARTICIPANT_USER = "org.hyot.network.User#"
VALUE_PARTICIPANT_NETWORKADMIN = "org.hyperledger.composer.system.NetworkAdmin#"
# Regex for the NGROK address
REGEX_NGROK_ADDRESS = "^(http:\/\/|https:\/\/)\w+\.ngrok\.io$"


########################################
#           GLOBAL VARIABLES           #
########################################
hlc_server_host = None                                  # Host where Hyperledger Composer REST server is running
hlc_server_port = None                                  # Port where Hyperledger Composer REST server is running
hlc_server_url = None                                   # Full address where Hyperledger Composer REST server is running
hlc_api_key = None                                      # Api key for Composer REST server


########################################
#               FUNCTIONS              #
########################################
def __is_jsonable(response):
    """
    Checks if the response is a JSON serializable and contains the 'participant' key.

    :param response: Response of the request.

    :return: True, if the response is a JSON serializable and contains the specified key. False, otherwise.
    """

    global KEY_PARTICIPANT

    try:
        # Serializes the response in JSON format
        response_json = response.json()

        # Checks if the key exists
        return bool(KEY_PARTICIPANT in response_json)
    except ValueError:
        return False


def __hlc_ping():
    """
    Checks if the address belongs to a business network of Hyperledger Fabric through running a ping with REST API
    exposed by the Hyperledger Composer REST server.

    :return: True, if the address belongs to a business network. False, otherwise.
    """

    global HLC_API_PING, REGEX_VALUE_PARTICIPANT_USER, REGEX_VALUE_PARTICIPANT_NETWORKADMIN, VALUE_PARTICIPANT_USER,\
        VALUE_PARTICIPANT_NETWORKADMIN, KEY_PARTICIPANT, hlc_server_url, hlc_api_key

    # Headers of the GET request
    if hlc_api_key:

        # REST server protected with API key
        headers = {
            'Accept': 'application/json',
            'x-api-key': hlc_api_key,
        }
    else:
        headers = {
            'Accept': 'application/json',
        }

    print("        Pinging the business network of the address: " + hlc_server_url)

    # GET request - Ping
    response = requests.get(hlc_server_url + HLC_API_PING, headers=headers)

    # Error 401 - Unauthorized request
    if response.status_code == requests.codes.unauthorized:
        print(Fore.RED + "        ✖ Error 401: Unauthorized request. Please, enter a valid API key or credentials to"
                         " submit the request to the Hyperledger Composer REST server." + Fore.RESET)
        sys.exit(0)

    # Error 404 - Not found
    elif response.status_code == requests.codes.not_found:
        print(Fore.RED + "        ✖ Error 404: Not found. Please, verify in the code that the URL is right and can be"
                         " found on the Hyperledger Composer REST server." + Fore.RESET)
        sys.exit(0)

    # Checks if the response is a JSON serializable and contains a specified key
    elif __is_jsonable(response):

        # Request is OK (200) and the 'participant' key contains a regular expression
        if (response.status_code == requests.codes.ok and
           (re.match(r"%s" % REGEX_VALUE_PARTICIPANT_USER, response.json()[KEY_PARTICIPANT]) or
               re.match(r"%s" % REGEX_VALUE_PARTICIPANT_NETWORKADMIN, response.json()[KEY_PARTICIPANT]))):

            print(Fore.GREEN + "        ✓ Business network is alive in the address" + Fore.RESET)

        else:
            if "error" in (response.json()):
                print(Fore.RED + "        ✖ Wrong request. Error: " + str(response.status_code) + ". " +
                      str(response.json()['error']['name']) + ": " + str(response.json()['error']['message']) + "." +
                      Fore.RESET)
            else:
                print(Fore.RED + "        ✖ Participant key in the response does not contain the following"
                      " expressions: " + VALUE_PARTICIPANT_NETWORKADMIN + " or " + VALUE_PARTICIPANT_USER + "."
                      + Fore.RESET)
            sys.exit(0)

    else:
        print(Fore.RED + "        ✖ Response of Ping request is not a JSON serializable or it does not contain the"
                         " 'participant' key." + Fore.RESET)
        sys.exit(0)


def __port_isdigit(port):
    """
    Checks if the given port is a number.

    :param port: Port of the address.

    :return: True if the string only contains digits. False, otherwise.
    """
    return port.replace(".", "", 1).isdigit()


def __check_ngrok_address(host):
    """
    Checks if the address belongs to the NGROK tool.

    :param host: Host address typed by the user.

    :return: True, to indicate that the host is a NGROK address. False, otherwise.
    """

    global REGEX_NGROK_ADDRESS

    return bool(re.match(r"%s" % REGEX_NGROK_ADDRESS, host))


def __apikey_yes_no():
    """
    Asks the user a yes/no question for the creation of an API key to provide a first layer of security to access the
    REST API. Default value is yes.

    :return: True, if the user wants to generate an API KEY. False, otherwise.
    """

    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    while True:

        choice = raw_input(Fore.BLUE + "        Do you want to generate an API KEY for Composer REST server? " +
                           Fore.WHITE + "(Y/n) " + Fore.RESET).lower()

        if choice == '':
            return True
        elif choice in valid:
                return valid[choice]
        else:
            print(Fore.RED + "        Please, respond with 'yes' or 'no' (or 'y' or 'n')\n" + Fore.RESET)


def init():
    """
    Checks if Hyperledger Fabric is alive through running a ping with REST API exposed by the Hyperledger Composer
    REST server. This REST server allows to interact with the business network deployed in the Blockchain of Hyperledger
    Fabric.
    """

    global HTTP, HTTPS, HTTP_PORT, HTTPS_PORT, HLC_HOST, HLC_PORT, hlc_server_host, hlc_server_port, hlc_server_url,\
        hlc_api_key

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Checking if the business network in Hyperledger Fabric is alive"
          + Style.RESET_ALL)

    # Asks the user for the creation of an API key to provide a first layer of security to access the REST API
    choice = __apikey_yes_no()

    if choice:
        # Generates a random URL-safe text-string with 32 random bytes
        hlc_api_key = token.token_urlsafe()

        print("        Please, run the Composer REST server with the following API key: " + Fore.GREEN + hlc_api_key
              + Fore.RESET)

    # Asks the user for the host where Hyperledger Composer REST server is running
    hlc_server_host = raw_input(Fore.BLUE + "        Enter the host (e.g. IP or ngrok address) where Hyperledger "
                                            "Composer REST server is running: " + Fore.WHITE + "(" + HLC_HOST + ") "
                                + Fore.RESET) or HLC_HOST

    # Checks if the host is empty
    if hlc_server_host.isspace():
        print(Fore.RED + "        ✖ The host of the Hyperledger Composer REST server can not be empty." + Fore.RESET)
        sys.exit(0)

    # Asks the user for the port where Hyperledger Composer REST server is running
    hlc_server_port = raw_input(Fore.BLUE + "        Enter the port where Hyperledger Composer REST server is running: "
                                + Fore.WHITE + "(" + str(HLC_PORT) + ") " + Fore.RESET) or HLC_PORT

    # Checks if the port is empty
    if str(hlc_server_port).isspace():
        print(Fore.RED + "        ✖ The port of the Hyperledger Composer REST server can not be empty." + Fore.RESET)
        sys.exit(0)

    # Checks if the port is a number
    if not __port_isdigit(str(hlc_server_port)):
        print(Fore.RED + "        ✖ The port of the Hyperledger Composer REST server can only be a number."
              + Fore.RESET)
        sys.exit(0)

    # Checks if the address belongs to the NGROK tool
    ngrok_address = __check_ngrok_address(hlc_server_host)

    if ngrok_address:         # Ngrok address

        if int(hlc_server_port) != HTTP_PORT and int(hlc_server_port) != HTTPS_PORT:
            print(Fore.RED + "        ✖ The port of NGROK must be 80 for HTTP connections or 443 for HTTPS connections."
                  + Fore.RESET)
            sys.exit(0)

        # Full address
        hlc_server_url = hlc_server_host

        # Removes the substrings
        hlc_server_host = hlc_server_host.replace(HTTP, "").replace(HTTPS, "")

    else:                     # Address is IP:Port

        # Removes the substrings
        hlc_server_host = hlc_server_host.replace(HTTP, "").replace(HTTPS, "")
        # Full address TODO
        hlc_server_url = HTTP + hlc_server_host + ":" + str(hlc_server_port)

    # Checks if this host and port is alive and listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Creates an INET socket of type STREAM
    sock.settimeout(2)                                             # Set a timeout (2 sec) on blocking socket operations

    try:
        print("        Checking if this host and port is alive and listen")

        # Connects to a remote socket at address
        result_connection = sock.connect_ex((hlc_server_host, int(hlc_server_port)))

        # Host and port is running and alive
        if result_connection == 0:
            print(Fore.GREEN + "        ✓ Port " + str(hlc_server_port) + " in " + str(hlc_server_host) + " reachable"
                  + Fore.RESET)

            # Checks if this address belongs to Hyperledger Composer REST server
            __hlc_ping()
        else:
            print(Fore.RED + "        ✖ Connection closed in this address. Error on connect: " + str(result_connection)
                  + "." + Fore.RESET)
            sys.exit(0)
    except socket.gaierror:
        print(Fore.RED + "        ✖ Given host is invalid." + Fore.RESET)
        sys.exit(1)
    finally:
        sock.close()                                               # Closes the socket


def publishAlert_transaction(uuid, timestamp, alert_origin, hash_video, link):
    """
    Submits a transaction to publish a new alert asset in the Blockchain of Hyperledger Fabric.

    :param uuid: Identifier of the alert.
    :param timestamp: Datetime of the alert.
    :param alert_origin: Indicates the sensor that triggered the alert.
    :param hash_video: Hash of the content of the video.
    :param link: Link to the Cloud (e.g. Dropbox) where the file was uploaded.
    """

    global HLC_API_PUBLISH_ALERT, hlc_server_url, hlc_api_key

    # Headers of the POST request
    if hlc_api_key:

        # REST server protected with API key
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-api-key': hlc_api_key,
        }
    else:
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
            "link": link,
            "owner": 'resource:org.hyot.network.User#jesusiglesias',
        }
    }

    print(Fore.LIGHTBLACK_EX + "     -- Submitting the transaction to publish the alert to the Blockchain of"
                               " Hyperledger Fabric" + Fore.RESET),
    time.sleep(0.5)

    # POST request - PublishAlert transaction TODO - API Namespace
    response = requests.post(hlc_server_url + HLC_API_PUBLISH_ALERT, headers=headers,
                             data=json.dumps(payload))

    # Request is OK (200)
    if response.status_code == requests.codes.ok:
        print(Fore.GREEN + " ✓" + Fore.RESET)

    # Error 401 - Unauthorized request
    elif response.status_code == requests.codes.unauthorized:
        print(Fore.RED + " ✖ Error to submit the transaction. Error 401: Unauthorized request. Please, enter a valid"
                         " credentials to submit the request to the Hyperledger Composer REST server." + Fore.RESET)
        sys.exit(0)  # TODO Logger

    # Error 404 - Not found
    elif response.status_code == requests.codes.not_found:
        print(Fore.RED + " ✖ Error to submit the transaction. Error 404: Not found. Please, verify that the URL is"
                         " right and can be found on the Hyperledger Composer REST server." + Fore.RESET)
        sys.exit(0)  # TODO Logger

    else:
        print(Fore.RED + " ✖ Error to submit the transaction (code " + str(response.status_code) + "). "
              + str(response.json()['error']['message']) + "." + Fore.RESET)
        sys.exit(0)  # TODO Logger


def file_hash(video):
    """
    Applies a hash function to the content of the file.

    :param video: File to hash.

    :return: Hash of the video file.
    """

    global BLOCKSIZE

    try:
        print(Fore.LIGHTBLACK_EX + "     -- Applying a hash function to the content of the video" + Fore.RESET),

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

        print(Fore.RED + " ✖ Error to apply the hash function to the video: " + str(hashError) + "." + Fore.RESET)
        sys.exit(1)  # TODO Logger
