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
#           FILE:     gpg_module.py                                                                                    #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to make use of the functionality provided by the GNU Privacy      #
#                     Guard (GPG or GnuPG)                                                                             #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Access to a compatible version of the GnuPG executable                                           #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     02/03/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic to make use of the functionality provided by the GNU Privacy Guard (GPG or GnuPG)"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import email_module as email                    # Module to send emails
    import getpass                                  # Portable password input
    import gnupg                                    # GnuPG’s key management, encryption and signature functionality
    import qrcode                                   # Pure python QR Code generator
    import os                                       # Miscellaneous operating system interfaces
    import time                                     # Time access and conversions
    import yaml                                     # YAML parser and emitter for Python
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in gpg_module: " + importError.message.lower() + ".")
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
    print(Fore.RED + "✖ The configuration file (conf/hyot.yml) has not the YAML format." + Fore.RESET)
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
# Path where GPG will store the public and private keyring files and a trust database. Hidden directory in user’s home
# directory
GPGDIRDEFAULT = os.path.expanduser('~') + "/.gpg"
PUBKEYRING = "pub_hyot.gpg"                                             # Public keyring
SECKEYRING = "sec_hyot.gpg"                                             # Secret keyring
KEYSFILE = "hyot_keys.asc"                                              # File with the public and private keys
QRIMAGE = "hyot_qr.png"                                                 # QR image
GPGEXT = "gpg"                                                          # Extension of the encrypted file

try:
    NAME = conf['gpg']['name']                                          # Name
    EMAIL = conf['gpg']['email']                                        # Email id

except (KeyError, TypeError) as keyError:
    print(Fore.RED + "✖ Please, make sure that the keys: [gpg|name] and [gpg|email] exist in the configuration file "
                     "(conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
gpg = None                                                       # GPG instance
keyid = None                                                     # Fingerprint of the GPG key
gpg_dir = None                                                   # GPG directory
keys_finalpath = None                                            # Path where the public and private key will be stored
qr_finalpath = None                                              # Path where the QR image will be stored
fingerprint_array = []                                           # Array to store the existing fingerprints


########################################
#               FUNCTIONS              #
########################################
def __request_validate_password():
    """
    Asks the user for the password for the private key and validates it based on a set of rules. User has 3 attempts.
    """

    # Variables
    min_length = 8                                               # Minimum length allowed for the password
    counter_pass = 0                                             # Counter of attempts
    counter_confirm_pass = 0                                     # Counter of attempts

    while True:

        # Asks the user for the password of the private key
        key_pass = getpass.getpass(Fore.BLUE + "        Enter the password for the private key: " + Fore.RESET) or None

        # Checks if the password is empty
        if key_pass is None or key_pass.isspace():
            print(Fore.RED + "        ✖ The password can not be empty." + Fore.RESET)
            sys.exit(0)

        # Removes the spaces
        key_pass = key_pass.replace(" ", "")

        if counter_pass > 2:
            print(Fore.RED + "        ✖ Number of attempts spent. Please, run again the code.\n" + Fore.RESET)
            sys.exit(0)
        elif len(key_pass) < min_length:                           # Checks for min length
            print(Fore.YELLOW + "        Password must be at least " + str(min_length) + " characters long."
                  + Fore.RESET)
            counter_pass = counter_pass + 1

        elif sum(c.isdigit() for c in key_pass) < 1:             # Checks for digit
            print(Fore.YELLOW + "        Password must contain at least 1 number." + Fore.RESET)
            counter_pass = counter_pass + 1

        elif not any(c.isupper() for c in key_pass):             # Checks for uppercase letter
            print(Fore.YELLOW + "        Password must contain at least 1 uppercase letter." + Fore.RESET)
            counter_pass = counter_pass + 1

        elif not any(c.islower() for c in key_pass):             # Checks for lowercase letter
            print(Fore.YELLOW + "        Password must contain at least 1 lowercase letter." + Fore.RESET)
            counter_pass = counter_pass + 1

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
            if counter_confirm_pass < 2:
                print(Fore.YELLOW + "        ✖ Passwords must match. Please, try it again." + Fore.RESET)
                counter_confirm_pass = counter_confirm_pass + 1
            else:
                print(Fore.RED + "        ✖ Number of attempts spent. Please, run again the code." + Fore.RESET)
                sys.exit(0)
        else:
            return key_pass


def __check_and_rename(qr, count=0):
    """
    Checks if the file exists in the path and if so it renames it adding the rule: [_number].

    :param qr: True, to indicate that the file belongs to the QR image. False, to indicate that belongs to the keys
     file.
    :param count: Number to add to the name.
    """

    global KEYSFILE, QRIMAGE, gpg_dir, keys_finalpath, qr_finalpath

    # Generates the new name
    if count != 0:
        if qr:
            split = QRIMAGE.split(".")
        else:
            split = KEYSFILE.split(".")

        rename = split[0] + "_" + str(count)
        filename = ".".join([rename, split[1]])
    else:
        if qr:
            filename = QRIMAGE
        else:
            filename = KEYSFILE

    # Possible final path
    filepath = gpg_dir + "/" + filename

    # Checks if a file exists with the same name
    if not os.path.isfile(filepath):
        if qr:
            qr_finalpath = filepath
        else:
            keys_finalpath = filepath

        return
    else:
        __check_and_rename(qr, count + 1)


def __generate_qrcode():
    """
    Generates a QR code of the fingerprint of the GPG key.
    """

    global keyid, qr_finalpath

    try:
        # Creates an image from the QR Code instance
        qr_image = qrcode.make(keyid)

        # Checks if the file exists in the path and if so it renames it adding the rule: [_number]
        __check_and_rename(True)

        # Stores the QR image
        qr_image.save(qr_finalpath)

        print("          - QR image of the fingerprint: " + Fore.CYAN + qr_finalpath.split("/")[-1] + Fore.RESET)

    except Exception as qrError:
        print(Fore.RED + "        ✖ Error to generate the QR image. Exception: " + str(qrError) + "." + Fore.RESET)
        sys.exit(1)


def __generate_keys():
    """
    Creates the GPG key and exports the public and private keys.
    """

    global KEYSFILE, NAME, EMAIL, gpg, gpg_dir, keyid, keys_finalpath

    # Asks the user for the password of the private key and validates it later
    private_key_pass = __request_validate_password()

    # Establishes the input data
    input_data = gpg.gen_key_input(name_real=NAME, name_email=EMAIL, passphrase=private_key_pass)
    key = gpg.gen_key(input_data)                                              # Creates the GPG key
    keyid = str(key.fingerprint)                                               # Obtains the fingerprint

    print(Fore.GREEN + "        ✓ GPG key created successfully with fingerprint: " + Fore.CYAN + keyid + Fore.RESET)
    print("        Files generated and stored in: " + gpg_dir)

    # Generates a QR code of the fingerprint
    __generate_qrcode()

    public_key = gpg.export_keys(keyid)                                        # Exports the fingerprint (public key)
    private_key = gpg.export_keys(keyid, True, passphrase=private_key_pass)    # Exports the fingerprint (private key)

    # Stores the keys in a file
    if public_key and private_key:

        # Checks if the file exists in the path and if so it renames it adding the rule: [_number]
        __check_and_rename(False)

        with open(keys_finalpath, 'w') as f:
            f.write(public_key)
            f.write(private_key)

        print("          - Public and private keys: " + Fore.CYAN + keys_finalpath.split("/")[-1] + '\n' + Fore.RESET)

        print(Fore.YELLOW + "        It's important that you remember the fingerprint and keep these files to decrypt "
                            "later." + Style.RESET_ALL)
    else:
        print(Fore.RED + "        ✖ Error to write the keys. Can't find key with fingerprint: " + str(keyid) + "." +
              Fore.RESET)
        sys.exit(0)


def __check_keys():
    """
    Checks if in the entered GPG directory some key already exists.
    """

    global gpg, keyid, fingerprint_array

    # Obtains the public keys
    public_keys = gpg.list_keys(False)

    # Obtains the private keys
    private_keys = gpg.list_keys(True)

    time.sleep(0.5)

    # Checks if the GPG directory has public and private keys (len(public_keys/private_keys) == 0)
    if not public_keys and not private_keys:
        print("        The GPG directory does not contain any GPG key. Generating a GPG key...")

        time.sleep(0.5)

        # Generates the key
        __generate_keys()
    else:
        print("        The GPG directory already contains some GPG key")

        time.sleep(0.5)

        key_input = raw_input(Fore.BLUE + "        Please, enter the fingerprint the key or keys (separated by commas)"
                                          " to use or empty to create a new one: " + Fore.RESET) or None

        # Checks if the user entered a fingerprint
        if key_input is None or key_input.isspace():
            print(Fore.BLACK + "        Generating a GPG key..." + Fore.RESET)

            # Generates the key
            __generate_keys()
        else:
            # Removes the spaces
            key_input = key_input.replace(" ", "")

            # Splits each entered fingerprint
            key_input = key_input.split(",")

            # Obtains the fingerprint of each private key stored in the keyring
            for key in private_keys:
                fingerprint_array.append(key['fingerprint'])

            # Checks if some entered fingerprint does not exist in the keyring
            for fingerprint in key_input:
                if fingerprint not in fingerprint_array:
                    print(Fore.RED + "        ✖ The fingerprint: " + fingerprint + " does not exist in the indicated"
                                     " GPG directory." + Fore.RESET)
                    sys.exit(0)

            # All fingerprints exist
            keyid = key_input


def init():
    """
    Creates the GPG instance and the public and private keys.
    """

    global GPGDIRDEFAULT, PUBKEYRING, SECKEYRING, gpg, gpg_dir

    try:
        print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing GPG" + Style.RESET_ALL)

        # Asks the user for the GPG directory
        gpg_dir = raw_input(Fore.BLUE + "        Enter the path of the directory used by GPG: " + Fore.WHITE +
                            "(" + GPGDIRDEFAULT + ") " + Fore.RESET) or GPGDIRDEFAULT

        # Checks if the path of the GPG directory is empty
        if gpg_dir.isspace():
            print(Fore.RED + "        ✖ The path of the GPG directory can not be empty." + Fore.RESET)
            sys.exit(0)

        # Removes the spaces
        gpg_dir = gpg_dir.replace(" ", "")

        # Establishes the permissions only if the directory already exists
        if os.path.exists(gpg_dir):
            os.chmod(gpg_dir, 0700)

        # Creates the GPG instance
        gpg = gnupg.GPG(gnupghome=gpg_dir, keyring=PUBKEYRING, secret_keyring=SECKEYRING)

        print(Fore.GREEN + "        ✓ Keyrings and trust database were successfully created" + Style.RESET_ALL)

        # Checks if in the entered GPG directory some key already exists
        __check_keys()

        time.sleep(1)

    except Exception as initGPGError:
        print(Fore.RED + "        ✖ Error to initialize the GPG module. Exception: " + str(initGPGError) + "."
              + Fore.RESET)
        sys.exit(1)

    print("\n        ------------------------------------------------------")


def encrypt_file(video, mailto):
    """
    Encrypts the file to upload to the Cloud (e.g. Dropbox).

    :param video: File to encrypt with its full path.
    :param mailto: Email address where to send the error notification if it occurs.

    :return: encrypted_file File whose content has been encrypted.
    """

    global GPGEXT, gpg, keyid

    try:
        # Path of the encrypted file
        encrypted_file = ".".join([video, GPGEXT])

        print(Fore.LIGHTBLACK_EX + "     -- Encrypting the video " + Fore.RESET),

        time.sleep(0.5)

        with open(video, 'rb') as f:
            status = gpg.encrypt_file(f, recipients=keyid, output=encrypted_file)

        if status.ok:
            print(Fore.GREEN + " ✓" + Fore.RESET)
            return encrypted_file
        else:
            print(Fore.RED + "✖ File not encrypted. Exception (status): " + str(status) + ".\n" + Fore.RESET)

            # Prints a message or sends an email when an error occurs during the alert procedure
            email.print_error_notification_or_send_email(mailto)

            sys.exit(0)  # TODO Logger

    except Exception as encryptError:
        print(Fore.RED + "✖ File not encrypted. Exception: " + str(encryptError) + ".\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert procedure
        email.print_error_notification_or_send_email(mailto)

        sys.exit(1)  # TODO Logger


def clean():
    """
    Cleans the GPG instance.
    """

    global gpg

    if not (gpg is None):
        print("      Cleaning the GPG instance"),

        time.sleep(0.25)

        try:
            gpg = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✖" + Fore.RESET)
            raise

        time.sleep(0.25)
