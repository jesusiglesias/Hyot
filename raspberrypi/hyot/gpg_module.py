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
#           FILE:     gpg_module.py                                                                                    #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to make use of the functionality provided by the GNU Privacy      #
#                     Guard (GPG or GnuPG)                                                                             #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Have access to a compatible version of the GnuPG executable                                      #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     02/03/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic to make use of the functionality provided by the GNU Privacy Guard (GPG or GnuPG)"""

########################################
#               IMPORTS                #
########################################

try:
    import sys                                      # System-specific parameters and functions
    import os                                       # Miscellaneous operating system interfaces
    import time                                     # Time access and conversions
    import gnupg                                    # GnuPG’s key management, encryption and signature functionality
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in gpg_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
# Path where GPG will store the public and private keyring files and a trust database
HOMEDIR = os.path.dirname(os.path.abspath(__file__)) + "/gpg"
PUBKEY = "pub_hyot.gpg"                                                 # Public key
SECKEY = "sec_hyot.gpg"                                                 # Secret key
KEYS = HOMEDIR + "/hyot_keys.asc"                                       # File with the public and private keys
NAME = "Hyot"                                                           # Name
EMAIL = "hyot.project@gmail.com"                                        # Email id
PASS = "h7y1ot13"                                                       # Passphrase of private key


########################################
#           GLOBAL VARIABLES           #
########################################
gpg = None                                                              # GPG instance


########################################
#               FUNCTIONS              #
########################################
def init():
    """Creates the GPG instance and the public and private keys"""

    global gpg, HOMEDIR, PUBKEY, SECKEY, KEYS, NAME, EMAIL, PASS

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing GPG" + Style.RESET_ALL)

    # Creates the GPG instance
    gpg = gnupg.GPG(gnupghome=HOMEDIR, keyring=PUBKEY, secret_keyring=SECKEY)

    print(Fore.GREEN + "        Key rings and trust database were created in: " + Style.BRIGHT
          + HOMEDIR + Style.RESET_ALL)

    # Establishes the input data
    input_data = gpg.gen_key_input(name_real=NAME, name_email=EMAIL, passphrase=PASS)
    key = gpg.gen_key(input_data)                                       # Creates the keys
    keyid = str(key.fingerprint)                                        # Obtains the fingerprint
    public_key = gpg.export_keys(keyid)                                 # Exports the fingerprint (public key)
    private_key = gpg.export_keys(keyid, True, passphrase=PASS)         # Exports the fingerprint (private key)

    # Stores the keys in a file
    if public_key and private_key:
        with open(KEYS, 'w') as f:
                f.write(public_key)
                f.write(private_key)

        print(Fore.GREEN + "        Public and private keys were stored in: " + Style.BRIGHT + KEYS + Style.RESET_ALL)
    else:
        print("Can't find key with fingerprint {}!".format(keyid))

    time.sleep(1)

    print("\n        ------------------------------------------------------")


def clean():
    """Cleans the GPG instance"""

    global gpg

    if not (gpg is None):
        print("        Cleaning the GPG instance"),

        time.sleep(0.25)

        try:
            gpg = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
