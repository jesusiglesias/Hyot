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
    import getpass                                  # Portable password input
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
GPGDIRDEFAULT = os.path.dirname(os.path.abspath(__file__)) + "/gpg"
PUBKEY = "pub_hyot.gpg"                                                 # Public key
SECKEY = "sec_hyot.gpg"                                                 # Secret key
KEYSFILE = "hyot_keys.asc"                                              # File with the public and private keys
NAME = "Hyot"                                                           # Name
EMAIL = "hyot.project@gmail.com"                                        # Email id
PASS = "h7y1ot13"                                                       # Passphrase of private key


########################################
#           GLOBAL VARIABLES           #
########################################
gpg = None                                                              # GPG instance
gpg_dir = None                                                          # GPG directory


########################################
#               FUNCTIONS              #
########################################
def generate_keys():
    """Creates the GPG key and exports the public and private keys"""

    global gpg, gpg_dir, KEYSFILE, NAME, EMAIL, PASS

    # Asks the user for the password of the private key
    private_key_pass = getpass.getpass(Fore.BLUE + "        Enter the password for the private key. Empty to use the "
                                                   "default value: " + Fore.RESET) or PASS

    # Checks if the password is empty
    if private_key_pass.isspace():
        print(Fore.RED + "        The password can not be empty" + Fore.RESET)
        sys.exit(1)

    # Removes the spaces
    private_key_pass = private_key_pass.replace(" ", "")

    # Establishes the input data
    input_data = gpg.gen_key_input(name_real=NAME, name_email=EMAIL, passphrase=private_key_pass)
    key = gpg.gen_key(input_data)                                              # Creates the GPG key
    keyid = str(key.fingerprint)                                               # Obtains the fingerprint

    print(Fore.GREEN + "        GPG key created successfully with fingerprint: " + Style.BRIGHT + keyid
          + Style.RESET_ALL)

    public_key = gpg.export_keys(keyid)                                        # Exports the fingerprint (public key)
    private_key = gpg.export_keys(keyid, True, passphrase=private_key_pass)    # Exports the fingerprint (private key)

    # Stores the keys in a file
    if public_key and private_key:

        keys_path = gpg_dir + "/" + KEYSFILE                                   # Path where the keys file will be stored

        with open(keys_path, 'w') as f:
            f.write(public_key)
            f.write(private_key)

        print(Fore.GREEN + "        Public and private keys were stored in: " + Style.BRIGHT + keys_path
              + Style.RESET_ALL)

    else:
        print(Fore.RED + "        Error to write the keys. Can't find key with fingerprint: " + keyid + Fore.RESET)
        sys.exit(1)


def init():
    """Creates the GPG instance and the public and private keys"""

    global gpg, gpg_dir, GPGDIRDEFAULT, PUBKEY, SECKEY, KEYSFILE

    try:
        print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing GPG" + Style.RESET_ALL)

        # Asks the user for the GPG directory
        gpg_dir = raw_input(Fore.BLUE + "        Enter the path of the directory used by GPG. Empty to use the default "
                                        "value (" + GPGDIRDEFAULT + "): " + Fore.RESET) or GPGDIRDEFAULT

        # Checks if the path of the GPG directory is empty
        if gpg_dir.isspace():
            print(Fore.RED + "        The path of the GPG directory can not be empty" + Fore.RESET)
            sys.exit(1)

        # Removes the spaces
        gpg_dir = gpg_dir.replace(" ", "")

        # Establishes the permissions only if the directory already exists
        if os.path.exists(gpg_dir):
            os.chmod(gpg_dir, 0700)

        # Creates the GPG instance
        gpg = gnupg.GPG(gnupghome=gpg_dir, keyring=PUBKEY, secret_keyring=SECKEY)

        print(Fore.GREEN + "        Key rings and trust database were created in: " + Style.BRIGHT + gpg_dir
              + Style.RESET_ALL)

        # Generates the key
        generate_keys()

        time.sleep(1)

    except Exception as initGPGError:
        print(Fore.RED + "        Error to initialize the GPG module: " + str(initGPGError) + Fore.RESET)
        sys.exit(1)

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
