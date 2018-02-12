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
PUBKEYRING = "pub_hyot.gpg"                                             # Public key ring
SECKEYRING = "sec_hyot.gpg"                                             # Secret key ring
KEYSFILE = "hyot_keys.asc"                                              # File with the public and private keys
NAME = "Hyot"                                                           # Name
EMAIL = "hyot.project@gmail.com"                                        # Email id
GPGEXT = "gpg"                                                          # Extension of the encrypted file


########################################
#           GLOBAL VARIABLES           #
########################################
gpg = None                                                       # GPG instance
keyid = None                                                     # Fingerprint of the GPG key
gpg_dir = None                                                   # GPG directory
keys_path = None                                                 # Path where the public and private key will be stored
fingerprint_array = []                                           # Array to store the existing fingerprints


########################################
#               FUNCTIONS              #
########################################
def request_validate_password():
    """Asks the user for the password for the private key and validates it based on a set of rules"""

    # Variables
    min_length = 8                                               # Minimum length allowed for the password
    counter = 0                                                  # Counter of attempts

    while True:

        # Asks the user for the password of the private key
        key_pass = getpass.getpass(Fore.BLUE + "        Enter the password for the private key: " + Fore.RESET) or None

        # Checks if the password is empty
        if key_pass is None or key_pass.isspace():
            print(Fore.RED + "        The password can not be empty." + Fore.RESET)
            sys.exit(0)

        # Removes the spaces
        key_pass = key_pass.replace(" ", "")

        if len(key_pass) < min_length:                           # Checks for min length
            print(Fore.YELLOW + "        Password must be at least " + str(min_length) + " characters long."
                  + Fore.RESET)

        elif sum(c.isdigit() for c in key_pass) < 1:             # Checks for digit
            print(Fore.YELLOW + "        Password must contain at least 1 number." + Fore.RESET)

        elif not any(c.isupper() for c in key_pass):             # Checks for uppercase letter
            print(Fore.YELLOW + "        Password must contain at least 1 uppercase letter." + Fore.RESET)

        elif not any(c.islower() for c in key_pass):             # Checks for lowercase letter
            print(Fore.YELLOW + "        Password must contain at least 1 lowercase letter." + Fore.RESET)

        else:
            break

    while True:

        # Asks again the user for the password of the private key
        confirm_pass = getpass.getpass(Fore.BLUE + "        Confirm the password for the private key: "
                                       + Fore.RESET) or None

        # Removes the spaces
        if not (confirm_pass is None):
            confirm_pass = confirm_pass.replace(" ", "")

        # Compares both passwords
        if key_pass != confirm_pass:
            if counter < 2:
                print(Fore.YELLOW + "        Passwords must match. Please, try it again." + Fore.RESET)
                counter = counter + 1
            else:
                print(Fore.RED + "        Number of attempts spent. Please, run again the code." + Fore.RESET)
                sys.exit(0)
        else:
            return key_pass


def check_and_rename(filepath, count=0):
    """Checks if the file exists in the path and if so it renames it adding the rule: [_number]
    :param filepath: Path of the file that will store the public and private key
    :param count: Number to add to the name
    """

    global keys_path

    # Saves the original path of the file
    original_filepath = filepath

    # Builds the new name
    if count != 0:
        split = filepath.split(".")
        name = split[0] + "_" + str(count)
        filepath = ".".join([name, split[1]])

    # Checks if a file exists with the same name
    if not os.path.isfile(filepath):
        keys_path = filepath
        return
    else:
        check_and_rename(original_filepath, count + 1)


def generate_keys():
    """Creates the GPG key and exports the public and private keys"""

    global gpg, gpg_dir, keyid, keys_path, KEYSFILE, NAME, EMAIL

    # Asks the user for the password of the private key and validates it later
    private_key_pass = request_validate_password()

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

        # Initial path where the keys will be stored
        keys_initial_path = gpg_dir + "/" + KEYSFILE

        # Checks if the file exists in the path and if so it renames it adding the rule: [_number]
        check_and_rename(keys_initial_path)

        with open(keys_path, 'w') as f:
            f.write(public_key)
            f.write(private_key)

        print(Fore.GREEN + "        Public and private keys were stored in: " + Style.BRIGHT + keys_path
              + Style.NORMAL + Fore.YELLOW + "\n        It's important that you remember the fingerprint and keep this "
                                             "file to decrypt later." + Style.RESET_ALL)
    else:
        print(Fore.RED + "        Error to write the keys. Can't find key with fingerprint: " + keyid + Fore.RESET)
        sys.exit(0)


def check_keys():
    """Checks if in the entered GPG directory some key already exists"""

    global gpg, keyid, fingerprint_array

    # Obtains the public keys
    public_keys = gpg.list_keys(False)

    # Obtains the private keys
    private_keys = gpg.list_keys(True)

    time.sleep(0.5)

    # Checks if the GPG directory has public and private keys
    if len(public_keys) == 0 and len(private_keys) == 0:
        print(Fore.BLACK + "        The GPG directory does not contain any GPG key. Generating a GPG key." + Fore.RESET)

        time.sleep(0.5)

        # Generates the key
        generate_keys()
    else:
        print(Fore.BLACK + "        The GPG directory already contains some GPG key." + Fore.RESET)

        time.sleep(0.5)

        key_input = raw_input(Fore.BLUE + "        Please, enter the fingerprint the key to use or empty to create"
                                          " a new one: " + Fore.RESET) or None

        # Checks if the user entered a fingerprint
        if key_input is None or key_input.isspace():
            print(Fore.BLACK + "        Generating a GPG key." + Fore.RESET)

            # Generates the key
            generate_keys()
        else:
            # Removes the spaces
            key_input = key_input.replace(" ", "")

            # Obtains the fingerprint of each private key
            for key in private_keys:
                fingerprint_array.append(key['fingerprint'])

            # Checks if the entered fingerprint exists in the key ring
            if key_input not in fingerprint_array:
                print(Fore.RED + "        The entered fingerprint does not exist in the indicated GPG directory."
                      + Fore.RESET)
                sys.exit(0)
            else:
                keyid = key_input


def init():
    """Creates the GPG instance and the public and private keys"""

    global gpg, gpg_dir, GPGDIRDEFAULT, PUBKEYRING, SECKEYRING

    try:
        print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing GPG" + Style.RESET_ALL)

        # Asks the user for the GPG directory
        gpg_dir = raw_input(Fore.BLUE + "        Enter the path of the directory used by GPG. Empty to use the default "
                                        "value (" + GPGDIRDEFAULT + "): " + Fore.RESET) or GPGDIRDEFAULT

        # Checks if the path of the GPG directory is empty
        if gpg_dir.isspace():
            print(Fore.RED + "        The path of the GPG directory can not be empty" + Fore.RESET)
            sys.exit(0)

        # Removes the spaces
        gpg_dir = gpg_dir.replace(" ", "")

        # Establishes the permissions only if the directory already exists
        if os.path.exists(gpg_dir):
            os.chmod(gpg_dir, 0700)

        # Creates the GPG instance
        gpg = gnupg.GPG(gnupghome=gpg_dir, keyring=PUBKEYRING, secret_keyring=SECKEYRING)

        print(Fore.GREEN + "        Key rings and trust database were created in: " + Style.BRIGHT + gpg_dir
              + Style.RESET_ALL)

        # Checks if in the entered GPG directory some key already exists
        check_keys()

        time.sleep(1)

    except Exception as initGPGError:
        print(Fore.RED + "        Error to initialize the GPG module: " + str(initGPGError) + Fore.RESET)
        sys.exit(1)

    print("\n        ------------------------------------------------------")


def encrypt_file(video):
    """Encrypts the file to upload to Dropbox
    :param video: File to encrypt with its full path
    """

    global gpg, keyid, GPGEXT

    try:
        # Path of the encrypted file
        encrypted_file = ".".join([video, GPGEXT])

        print(Fore.LIGHTBLACK_EX + "   -- Encrypting the video " + Fore.RESET),

        time.sleep(0.5)

        with open(video, 'rb') as f:
            status = gpg.encrypt_file(f, recipients=keyid, output=encrypted_file)

        if status.ok:
            print(Fore.GREEN + " ✓" + Fore.RESET)
            return encrypted_file
        else:
            print(Fore.RED + "✕ File not encrypted. The file will be stored in Dropbox without encrypting." + Fore.RESET)
            return video

    except Exception:
        print(Fore.RED + "✕ File not encrypted. The file will be stored in Dropbox without encrypting." + Fore.RESET)
        return video


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
