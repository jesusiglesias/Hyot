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
#        VERSION:     1.0.1                                                                                            #
#        CREATED:     01/18/18                                                                                         #
#       REVISION:     08/19/18                                                                                         #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic to interact with the Blockchain of Hyperledger Fabric"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import email_module as email                    # Module to send emails
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
    # Exception when making an unverified HTTPS request
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
DEFAULT_OWNER_ALERT_USERNAME = "hyotRPi"                # Default owner for the Alert assets - Username
DEFAULT_OWNER_ALERT_FIRST_NAME = "Hyot"                 # Default owner for the Alert assets - First name
DEFAULT_OWNER_ALERT_LAST_NAME = "Raspberry Pi"          # Default owner for the Alert assets - Last name
HLC_HOST = conf['hl']['host']                           # Default host where Hyperledger Composer REST server is running
HLC_PORT = conf['hl']['port']                           # Default port where Hyperledger Composer REST server is running
# Indicates if the certificate used in the Hyperledger Composer REST server is self-signed
HLC_SELFSIGNED_CERT = conf['hl']['selfsignedcert']
HLC_API_PING = "/api/system/ping"                       # Hyperledger Composer REST server API - Ping
# Hyperledger Composer REST server API - Publish alert transaction
HLC_API_PUBLISH_ALERT = "/api/org.hyot.network.PublishAlert"
HLC_API_CREATE_USER = "/api/org.hyot.network.User"
KEY_PARTICIPANT = "participant"                         # Key to search in a JSON format file
# Regex of the possible values that the 'participant key should contain
REGEX_VALUE_PARTICIPANT_USER = "^org\.hyot\.network\.User\#\w+$"
REGEX_VALUE_PARTICIPANT_NETWORKADMIN = "^org\.hyperledger\.composer\.system\.NetworkAdmin\#\w+$"
# Possible values that the 'participant key should contain
VALUE_PARTICIPANT_USER = "org.hyot.network.User#"
VALUE_PARTICIPANT_NETWORKADMIN = "org.hyperledger.composer.system.NetworkAdmin#"
# Regex for the NGROK address
REGEX_NGROK_ADDRESS = "^(http:\/\/|https:\/\/)\w+\.ngrok\.io$"
# Names to identify the step where the error has occurred
STEP_SUBMIT_ALERTTRANSACTION_UNAUTHORIZED = "Submit alert transaction to Hyperledger Fabric - Unauthorized"
STEP_SUBMIT_ALERTTRANSACTION_NOTFOUND = "Submit alert transaction to Hyperledger Fabric - Not found"
STEP_SUBMIT_ALERTTRANSACTION = "Submit alert transaction to Hyperledger Fabric"
STEP_HASH = "Generate hash code"

########################################
#           GLOBAL VARIABLES           #
########################################
hlc_server_host = None                                  # Host where Hyperledger Composer REST server is running
hlc_server_port = None                                  # Port where Hyperledger Composer REST server is running
hlc_server_url = None                                   # Full address where Hyperledger Composer REST server is running
hlc_api_key = None                                      # Api key for Composer REST server
verify_requests = None                                  # Verifies the identity of the certificate in the requests
owner_alert = None                                      # Owner of the alerts


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
        VALUE_PARTICIPANT_NETWORKADMIN, KEY_PARTICIPANT, hlc_server_url, hlc_api_key, verify_requests

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

    try:
        # GET request - Ping
        response = requests.get(hlc_server_url + HLC_API_PING, headers=headers, verify=verify_requests)
    except Exception as requestsError:
        print(Fore.RED + "        ✖ Error in GET request. Exception: " + str(requestsError) + "." + Fore.RESET)
        sys.exit(1)

    # Error 401 - Unauthorized request
    if response.status_code == requests.codes.unauthorized:
        print(Fore.RED + "        ✖ Error 401: Unauthorized request. Please, enter a valid API key to submit the"
                         " request to the Hyperledger Composer REST server." + Fore.RESET)
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
    REST API. Default value is yes. User has 3 attempts.

    :return: True, if the user wants to generate an API KEY. False, otherwise.
    """

    # Variables
    counter = 0                                         # Counter of attempts

    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    while True:

        choice = raw_input(Fore.BLUE + "        Do you want to generate an API KEY for Composer REST server? " +
                           Fore.WHITE + "(Y/n) " + Fore.RESET).lower()

        if choice == '':
            return True
        elif choice in valid:
            return valid[choice]
        else:
            if counter < 2:
                print(Fore.RED + "        ✖ Please, respond with 'yes' or 'no' (or 'y' or 'n').\n" + Fore.RESET)
                counter = counter + 1
            else:
                print(Fore.RED + "        ✖ Number of attempts spent. Please, run again the code.\n" + Fore.RESET)
                sys.exit(0)


def __createUser_participant(emailbc, firstname, lastname):
    """
    Creates a new User participant in the Blockchain.

    :param emailbc: Email of the user to register in the Blockchain.
    :param firstname: First name of the user to register in the Blockchain.
    :param lastname: Last name of the user to register in the Blockchain.
    """

    global owner_alert

    global HLC_API_CREATE_USER, STEP_SUBMIT_ALERTTRANSACTION_UNAUTHORIZED, STEP_SUBMIT_ALERTTRANSACTION_NOTFOUND,\
        STEP_SUBMIT_ALERTTRANSACTION, hlc_server_url, hlc_api_key, verify_requests, owner_alert

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
        "$class": 'org.hyot.network.User',
        "username": owner_alert,
        "email": emailbc,
        "first_name": firstname,
        "last_name": lastname
    }

    print("        Creating a new User participant in the Blockchain of Hyperledger Fabric")

    try:
        # POST request - Create User
        response = requests.post(hlc_server_url + HLC_API_CREATE_USER, headers=headers, data=json.dumps(payload),
                                 verify=verify_requests)
    except Exception as requestsError:
        print(Fore.RED + "        ✖ Error in POST request. Exception: " + str(requestsError) + "." + Fore.RESET)
        sys.exit(1)

    # Request is OK (200)
    if response.status_code == requests.codes.ok:

        print(Fore.GREEN + "        ✓ New participant created successfully: " + owner_alert + ". Use this username in"
                           " the web system or to register a normal user in this application." + Fore.RESET)

    # Error 401 - Unauthorized request
    elif response.status_code == requests.codes.unauthorized:
        print(Fore.RED + "        ✖ Error to create the participant. Error 401: Unauthorized request. Please,"
                         " enter a valid API key to submit the request to the Hyperledger Composer REST server."
              + Fore.RESET)

        sys.exit(0)

    # Error 404 - Not found
    elif response.status_code == requests.codes.not_found:
        print(Fore.RED + "        ✖ Error to create the participant. Error 404: Not found. Please, verify that the URL"
                         " is right and can be found on the Hyperledger Composer REST server." + Fore.RESET)

        sys.exit(0)

    else:  # E.g. Participant already exists with same username
        print(Fore.RED + "        ✖ Error to create the participant (code " + str(response.status_code) + ")."
                         " Exception: " + str(response.json()['error']['message']) + "." + Fore.RESET)

        sys.exit(0)


def __owner():
    """
    Asks the user for the owner of the alert assets and registers a new participant in the Blockchain.
    """

    global DEFAULT_OWNER_ALERT_USERNAME, DEFAULT_OWNER_ALERT_FIRST_NAME, DEFAULT_OWNER_ALERT_LAST_NAME, owner_alert

    # Asks the username for the owner
    owner_alert = raw_input(Fore.BLUE + "        Enter the username for the owner of the alerts: " + Fore.WHITE + "(" +
                            DEFAULT_OWNER_ALERT_USERNAME + ") " + Fore.RESET) or DEFAULT_OWNER_ALERT_USERNAME

    # Checks if the username is empty
    if owner_alert.isspace():
        print(Fore.RED + "        ✖ The owner can not be empty." + Fore.RESET)
        sys.exit(0)

    # Deletes all spaces
    owner_alert = owner_alert.replace(" ", "")

    # Asks the email for the owner
    owner_email = raw_input(Fore.BLUE + "        Enter the email for the owner of the alerts: " + Fore.WHITE +
                            "(optional)" + Fore.RESET) or None

    # Asks the first name for the owner
    owner_firstname = raw_input(Fore.BLUE + "        Enter the first name for the owner of the alerts: " + Fore.WHITE +
                                "(" + DEFAULT_OWNER_ALERT_FIRST_NAME + ") " + Fore.RESET)\
                      or DEFAULT_OWNER_ALERT_FIRST_NAME

    # Checks if the first name is empty
    if owner_firstname.isspace():
        print(Fore.RED + "        ✖ The first name can not be empty." + Fore.RESET)
        sys.exit(0)

    # Asks the last name for the owner
    owner_lastname = raw_input(Fore.BLUE + "        Enter the last name for the owner of the alerts: " + Fore.WHITE +
                               "(" + DEFAULT_OWNER_ALERT_LAST_NAME + ") " + Fore.RESET) or DEFAULT_OWNER_ALERT_LAST_NAME

    # Checks if the last name is empty
    if owner_lastname.isspace():
        print(Fore.RED + "        ✖ The last name can not be empty." + Fore.RESET)
        sys.exit(0)

    # Creates a new User participant in the Blockchain
    __createUser_participant(owner_email, owner_firstname, owner_lastname)


def init():
    """
    Checks if Hyperledger Fabric is alive through running a ping with REST API exposed by the Hyperledger Composer
    REST server. This REST server allows to interact with the business network deployed in the Blockchain of Hyperledger
    Fabric.
    """

    global HTTPS, HTTP, HTTP_PORT, HTTPS_PORT, HLC_HOST, HLC_PORT, HLC_SELFSIGNED_CERT, verify_requests,\
           hlc_server_host, hlc_server_port, hlc_server_url, hlc_api_key

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Checking if the business network in Hyperledger Fabric is alive"
          + Style.RESET_ALL)

    # Asks the user for the creation of an API key to provide a first layer of security to access the REST API
    choice = __apikey_yes_no()

    if choice:
        try:
            # Generates a random URL-safe text-string with 32 random bytes
            hlc_api_key = token.token_urlsafe()
            print("        Please, run the Composer REST server with the following API key: " + Fore.CYAN + hlc_api_key
                  + Fore.RESET)

        except Exception as tokenError:
            print(Fore.RED + "        ✖ Error to generate the API key. Exception: " + str(tokenError) + "."
                  + Fore.RESET)
            sys.exit(1)

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

    # Checks if the REST server is using a self-signed certificate
    verify_requests = not HLC_SELFSIGNED_CERT

    # Disables the warning message when making an unverified HTTPS request (self-signed certificate)
    if not verify_requests:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
        # Full address - Only HTTPS communications
        hlc_server_url = HTTPS + hlc_server_host + ":" + str(hlc_server_port)

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

    # Asks the user for the owner of the alert assets and registers a new participant in the Blockchain
    __owner()


def publishAlert_transaction(uuid, timestamp, sensor_origin, event_origin, hash_video, link, mailto):
    """
    Submits a transaction to publish a new alert asset in the Blockchain of Hyperledger Fabric.

    :param uuid: Identifier of the alert.
    :param timestamp: Datetime of the alert.
    :param sensor_origin: Indicates the sensor that triggered the alert.
    :param event_origin: Indicates the event of the sensor that triggered the alert.
    :param hash_video: Hash of the content of the video.
    :param link: Link to the Cloud (e.g. Dropbox) where the file was uploaded.
    :param mailto: Email address where to send the error notification if it occurs.
    """

    global HLC_API_PUBLISH_ALERT, STEP_SUBMIT_ALERTTRANSACTION_UNAUTHORIZED, STEP_SUBMIT_ALERTTRANSACTION_NOTFOUND,\
        STEP_SUBMIT_ALERTTRANSACTION, hlc_server_url, hlc_api_key, verify_requests, owner_alert

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
            "sensor_origin": sensor_origin,
            "event_origin": event_origin.upper(),
            "hash": hash_video,
            "link": link,
            "owner": 'resource:org.hyot.network.User#' + owner_alert,
        }
    }

    print(Fore.LIGHTBLACK_EX + "     -- Submitting the transaction to publish the alert to the Blockchain of"
                               " Hyperledger Fabric" + Fore.RESET),
    time.sleep(0.5)

    try:
        # POST request - PublishAlert transaction
        response = requests.post(hlc_server_url + HLC_API_PUBLISH_ALERT, headers=headers, data=json.dumps(payload),
                                 verify=verify_requests)
    except Exception as requestsError:
        print(Fore.RED + "        ✖ Error in POST request. Exception: " + str(requestsError) + "." + Fore.RESET)
        sys.exit(1)

    # Request is OK (200)
    if response.status_code == requests.codes.ok:
        print(Fore.GREEN + " ✓" + Fore.RESET)

    # Error 401 - Unauthorized request
    elif response.status_code == requests.codes.unauthorized:
        print(Fore.RED + " ✖ Error to submit the transaction. Error 401: Unauthorized request. Please, enter a valid"
                         " API key to submit the request to the Hyperledger Composer REST server.\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        email.print_error_notification_or_send_email(mailto, STEP_SUBMIT_ALERTTRANSACTION_UNAUTHORIZED)
        sys.exit(0)

    # Error 404 - Not found
    elif response.status_code == requests.codes.not_found:
        print(Fore.RED + " ✖ Error to submit the transaction. Error 404: Not found. Please, verify that the URL is"
                         " right and can be found on the Hyperledger Composer REST server.\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        email.print_error_notification_or_send_email(mailto, STEP_SUBMIT_ALERTTRANSACTION_NOTFOUND)
        sys.exit(0)

    else:  # E.g. Transaction already exists with same ID (Alert)
        print(Fore.RED + " ✖ Error to submit the transaction (code " + str(response.status_code) + "). Exception: "
              + str(response.json()['error']['message']) + ".\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        email.print_error_notification_or_send_email(mailto, STEP_SUBMIT_ALERTTRANSACTION)
        sys.exit(0)


def file_hash(video, mailto):
    """
    Applies a hash function to the content of the file.

    :param video: File to hash.
    :param mailto: Email address where to send the error notification if it occurs.

    :return: Hash of the video file.
    """

    global BLOCKSIZE, STEP_HASH

    try:
        print(Fore.LIGHTBLACK_EX + "     -- Applying a hash function to the content of the evidence" + Fore.RESET),

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
        print(Fore.RED + " ✖ Error to apply the hash function to the evidence. Exception: " + str(hashError) + ".\n"
              + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        email.print_error_notification_or_send_email(mailto, STEP_HASH)

        sys.exit(1)
