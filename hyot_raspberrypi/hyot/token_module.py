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
#           FILE:     token_module.py                                                                                  #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module provides a number of functions for generating secure tokens, suitable for            #
#                     applications such as password resets, access to APIs, hard-to-guess URLs, and similar            #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded by the script: hyperledgerFabric_module.py                                     #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     06/03/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module provides a number of functions for generating secure tokens, suitable for applications such as password
   resets, access to APIs, hard-to-guess URLs, and similar"""

########################################
#               IMPORTS                #
########################################
try:

    import sys                                      # System-specific parameters and functions
    import base64                                   # RFC 3548: Base16, Base32, Base64 Data Encodings
    import binascii                                 # Convert between binary and ASCII
    import os                                       # Miscellaneous operating system interfaces

except ImportError as importError:
    print("Error to import in token_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
DEFAULT_ENTROPY = 32                                    # Number of bytes to return by default


########################################
#               FUNCTIONS              #
########################################
def token_bytes(nbytes=None):
    """
    Returns a random byte-string containing 'nbytes' number of bytes.

    :param nbytes: Number of bytes of the token.

    :return: Random byte-string.
    """

    if nbytes is None:
        nbytes = DEFAULT_ENTROPY

    return os.urandom(nbytes)


def token_hex(nbytes=None):
    """
    Returns a random text-string in hexadecimal. The string has 'nbytes' random bytes, each byte converted to two
    hex digits.

    :param nbytes: Number of bytes of the token.

    :return: Random text-string in hexadecimal.
    """

    return binascii.hexlify(token_bytes(nbytes)).decode('ascii')


def token_urlsafe(nbytes=None):
    """
    Returns a random URL-safe text-string, containing 'nbytes' random bytes. On average, each byte results in
    approximately 1.3 characters in the final result.

    :param nbytes: Number of bytes of the token.

    :return: Random URL-safe text-string.
    """

    # Random byte-string
    tok = token_bytes(nbytes)

    return base64.urlsafe_b64encode(tok).rstrip(b'=').decode('ascii')
