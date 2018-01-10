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
#   REQUIREMENTS:     ---                                                                                              #
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
    print("Error to import: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
TOKEN = "eI5UZqDlaNAAAAAAAAAAJm2xSwyCoMquSwWq7p270YXf5qr3p1vawOu5AzS99Uih"   # Authorisation token


########################################
#               FUNCTIONS              #
########################################
def connect():
    """Creates an instance of the Dropbox class and establishes a connection"""

    global dbx

    print("      - Generating the client of the Dropbox service")

    # Asks the user for Dropbox token
    token = raw_input(Fore.BLUE + "        Enter the Dropbox token or empty to use the default value: "
                      + Fore.RESET) or TOKEN

    # Creates an instance of the Dropbox class, which can make requests to API
    dbx = dropbox.Dropbox(token)

    try:

        # Checks that the access token is valid
        current_user = dbx.users_get_current_account()

        print(Fore.GREEN + "        Dropbox client connected with the user: " + current_user.name.given_name
              + Fore.RESET)

        time.sleep(1)

    except dropbox.exceptions.AuthError as authError:

        # Checks if the error is due to an invalid token
        if authError.error.is_invalid_access_token():               # Access token has been revoked
            print(Fore.RED + "        " + "The introduced access token is invalid because it has been revoked"
                  + Fore.RESET)
            sys.exit(1)
        else:                                                       # Another error. For example: no write permission
            raise


def disconnect():
    """Disconnects the Dropbox client disabling the access token used to authenticate the calls"""

    global dbx

    if not (dbx is None):
        print("        Disconnecting the Dropbox client")

        # Ends the client session
        dbx = None

        print(Fore.GREEN + "        Dropbox session ends successfully" + Fore.RESET)
