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
#                                  ____                             _   _                                              #
#                                 |  _ \  ___  ___ _ __ _   _ _ __ | |_(_) ___  _ __                                   #
#                                 | | | |/ _ \/ __| '__| | | | '_ \| __| |/ _ \| '_ \                                  #
#                                 | |_| |  __/ (__| |  | |_| | |_) | |_| | (_) | | | |                                 #
#                                 |____/ \___|\___|_|   \__, | .__/ \__|_|\___/|_| |_|                                 #
#                                                       |___/|_|                                                       #
#                                                                                                                      #
#                                                                                                                      #
#        PROJECT:     Hyot                                                                                             #
#           FILE:     hyot_decryption.py                                                                               #
#                                                                                                                      #
#          USAGE:     sudo python hyot_decryption.py                                                                   #
#                                                                                                                      #
#    DESCRIPTION:     This script decrypts a file previously encrypted with GPG                                        #
#                                                                                                                      #
#        OPTIONS:     Type '-h' or '--help' option to show the help                                                    #
#   REQUIREMENTS:     Root user, Access to a compatible version of the GnuPG executable, Encrypted file with GPG,      #
#                     Valid key or fingerprint and hash, Module: menu_module.py                                        #
#          NOTES:     ---                                                                                              #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     02/06/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This script decrypts a file previously encrypted with GPG"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import getpass                                  # Portable password input
    import gnupg                                    # GnuPG’s key management, encryption and signature functionality
    import hashlib                                  # Secure hashes and message digests
    import menu_module as menu                      # Module to execute initial checks and to parse the menu
    import os                                       # Miscellaneous operating system interfaces
    import sha3                                     # SHA-3 wrapper (Keccak) for Python
    import time                                     # Time access and conversions
    import traceback                                # Print or retrieve a stack traceback
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in hyot_decryption: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
PUBKEYRING = "pub_hyot.gpg"                         # Public key ring
SECKEYRING = "sec_hyot.gpg"                         # Secret key ring
EXT = ".gpg"                                        # Extension of a GPG file
BLOCKSIZE = 65536                                   # Block size (64kb) to hash


########################################
#           GLOBAL VARIABLES           #
########################################
gpg = None                                          # GPG instance
gpg_dir = None                                      # GPG directory
password = None                                     # Password of the private key
keys = None                                         # Path of the file which stores the public and private key
fingerprint = None                                  # Fingerprint of the private key to use
fingerprint_array = []                              # Array to store the existing fingerprints
encrypted_file = None                               # Path of the encrypted file with GPG
hash_file = None                                    # Hash code of the encrypted file
decrypted_dir = None                                # Directory where the decrypted file will be store
output_file = None                                  # Full path (path + filename) where the decrypted file will be store


########################################
#               FUNCTIONS              #
########################################
def check_root():
    """
    Checks that the script is run with a root user.
    """

    if not os.geteuid() == 0:
        print(Fore.RED + "✖ You need to have root privileges to run this script. Please, try it again using sudo."
              + Fore.RESET)
        sys.exit(0)


def header():
    """
    Prints the header in the console.
    """

    banner = """
    _    ___     ______ _______
   | |  | \ \   / / __ \__   __|
   | |__| |\ \_/ / |  | | | |
   |  __  | \   /| |  | | | |
   | |  | |  | | | |__| | | |
   |_|  |_|  |_|  \____/  |_|


   A PoC for traceability in IoT environments through Hyperledger by:

   - Jesús Iglesias García, jesusgiglesias@gmail.com

   -----------------------------------------------------

   HYOT - DECRYPTION

   This script allows to decrypt a file previously encrypted with GPG.

    """

    # Header
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + banner + Style.RESET_ALL)

    # Wait time - 1 second
    time.sleep(1)


def __check_existence():
    """
    Checks if the GPG directory, the file with the private and public key, the encrypted file and the directory,
    where the decrypted file will be store, exist in the local system.
    """

    global gpg_dir, keys, encrypted_file, decrypted_dir

    # Checks if the GPG directory exists
    if not os.path.isdir(gpg_dir):
        print(Fore.RED + "   ✖ The entered GPG directory does not exist or is not a directory in the local system.\n"
              + Fore.RESET)
        sys.exit(0)

    # Checks if the file, which must contain the public and private key, exists
    if keys:
        if not os.path.isfile(keys):
            print(Fore.RED + "   ✖ The entered key file does not exist or is not a file in the local system.\n"
                  + Fore.RESET)
            sys.exit(0)

    # Checks if the encrypted file exists
    if not os.path.isfile(encrypted_file):
        print(Fore.RED + "   ✖ The encrypted file does not exist or is not a file in the local system.\n" + Fore.RESET)
        sys.exit(0)

    # Checks if the directory, where the decrypted file will be store, exists
    if not os.path.isdir(decrypted_dir):
        print(Fore.RED + "   ✖ The directory, where the decrypted file will be store, does not exist or is not a "
                         "directory in the local system.\n" + Fore.RESET)
        sys.exit(0)


def __check_extension():
    """
    Checks if the encrypted file has the right extension.
    """

    global EXT, encrypted_file

    # Obtains the extension
    ext = os.path.splitext(encrypted_file)[-1].lower()

    if ext != EXT:
        print(Fore.RED + "   ✖ The encrypted file has an extension which is not allowed. It must be a file with "
                         "format: .gpg.\n" + Fore.RESET)
        sys.exit(0)


def __check_fingerprint():
    """
    Checks if the GPG directory has private keys and if the entered fingerprint exists.
    """

    global gpg, fingerprint, fingerprint_array

    # Obtains the private keys
    private_keys = gpg.list_keys(True)

    # Checks if the GPG directory has private keys (len(private_keys) == 0)
    if not private_keys:
        print(Fore.RED + "   ✖ The GPG directory does not contain any private key. Please, import the private key to "
                         "decrypt the file (option: -k/--keys).\n" + Fore.RESET)
        sys.exit(0)

    # Obtains the fingerprint of each private key
    for key in private_keys:
        fingerprint_array.append(key['fingerprint'])

    # Checks if the entered fingerprint exists in the key ring
    if fingerprint not in fingerprint_array:
        print(Fore.RED + "   ✖ The entered fingerprint does not exist in the indicated GPG directory. Please, import"
                         " the private key to decrypt the file or use another fingerprint.\n" + Fore.RESET)
        sys.exit(0)


def __import_keys():
    """
    Import the public and private keys from a file.
    """

    global gpg, keys

    keys_data = open(keys, 'rb').read()
    import_result = gpg.import_keys(keys_data)

    if import_result.count != 2:
        print(Fore.RED + "   ✖ The entered key file does not contain two keys (public and private key). Please, use"
                         " the generated file during the initialization of GPG.\n" + Fore.RESET)
        sys.exit(0)


def __request_password():
    """
    Asks the user for the password of the private key.
    """

    global password

    # Variables
    flag = False            # Flag for the loop
    counter = 0             # Counter of attempts

    while not flag:

        # Asks the user for the password of the private key
        password = getpass.getpass(Fore.BLUE + "      Enter the password for the private key: " + Fore.RESET) or None

        # Checks if the password is empty
        if password is None or password.isspace():

            if counter < 2:
                print(Fore.RED + "      ✖ The password can not be empty. Please, try it again.\n" + Fore.RESET)
                counter = counter + 1
            else:
                print(Fore.RED + "      ✖ Number of attempts spent. Please, run again the code.\n" + Fore.RESET)
                sys.exit(0)
        else:
            # Removes the spaces
            password = password.replace(" ", "")
            # Breaks out of while loop
            flag = True


def __compare_hash():
    """
    Obtains the hash code of the decrypted file and compares it with the one entered by the user.

    :return: True, to indicate that the decrypted file has not altered -stay unchanged-. False, otherwise.
    """

    global BLOCKSIZE, output_file, hash_file

    try:

        print(Style.BRIGHT + Fore.BLACK + "\n      - Comparing hash codes" + Style.RESET_ALL),

        time.sleep(1)

        # Variables
        hasher = hashlib.sha3_512()

        # Opens the file in read and binary mode
        with open(output_file, 'rb', buffering=0) as f:

            # Reads chunks of a certain size (64kb) to avoid memory failures when not knowing the size of the file
            for b in iter(lambda: f.read(BLOCKSIZE), b''):
                hasher.update(b)                                   # Updates the hash

        # Compares both hash codes
        if hasher.hexdigest() == hash_file:                        # Original file has not been altered

            print(Fore.GREEN + " ✓" + Fore.RESET)
            print("\n      Both hash codes are the same. The downloaded file has not been altered and its integrity is"
                  " guaranteed.\n")

        else:                                                      # Original file has been altered
            print(Fore.YELLOW + " " + u"\u26A0" + Fore.RESET)
            print("\n      Both hash codes are different. The downloaded file may have been manipulated by a malicious"
                  " third party and therefore its integrity is not guaranteed.\n")

    except Exception as hashError:

        print(Fore.RED + " ✕")
        print("\n      ✖ Error to calculate the hash code of the encrypted file. Error: " + str(hashError) + ".\n"
              + Fore.RESET)


def __decrypt_file():
    """
    Decrypts the file using the entered fingerprint or the imported key from a file.
    """

    global gpg, password, encrypted_file, output_file

    print(Style.BRIGHT + Fore.BLACK + "\n      - Decrypting" + Style.RESET_ALL),

    with open(encrypted_file, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=password, output=output_file)

        if not status.ok:

            print(Fore.RED + " ✕")
            print("\n      The decryption has failed. Main reasons: \n")
            print("       - File was encrypted with another RSA key.")
            print("       - Bad passphrase to unlock the GPG secret key.")
            print("       - No valid OpenPGP data found.")
            print("       - Output is a directory.\n" + Fore.RESET)
            sys.exit(0)
        else:
            print(Fore.GREEN + " ✓" + Fore.RESET)
            print("\n      File successfully decrypted in the path: " + str(output_file) + ".")


def main(user_args):
    """
    Main function.

    :param user_args: Values of the options entered by the user.
    """

    global PUBKEYRING, SECKEYRING, gpg, gpg_dir, fingerprint, keys, encrypted_file, hash_file, decrypted_dir,\
        output_file

    # Try-Catch block
    try:

        # Variables
        gpg_dir = user_args.GPGHOME
        fingerprint = user_args.FINGERPRINT
        keys = user_args.KEYS
        encrypted_file = user_args.ENCRYPTEDFILE
        hash_file = user_args.HASHFILE
        decrypted_dir = user_args.DECRYPTEDHOME

        # Header
        header()

        print(Style.BRIGHT + Fore.BLACK + "   -- Initializing the decryption...\n" + Style.RESET_ALL)

        time.sleep(1)

        # Checks if the directory, which will store the decrypted file, has been entered by the user (optional argument)
        if not decrypted_dir:
            # Obtains the directory from the encrypted file, removing the file
            decrypted_dir = "/".join(encrypted_file.split("/")[:-1])

            # Full path where the decrypted file will be stored. It removes the extension: .gpg
            output_file = os.path.splitext(encrypted_file)[0]
        else:
            # Full path where the decrypted file will be stored. Takes the name of the encrypted file removing the
            # extension '.gpg' and adds it to the directory that will store the decrypted file
            output_file = "/".join([decrypted_dir, os.path.splitext(encrypted_file.split("/")[-1])[0]])

            output_file = output_file.replace("//", "/")

        # Checks if the entered directories and files exist in the local system
        __check_existence()

        # Checks if the encrypted file has the right extension (.gpg)
        __check_extension()

        # Creates the GPG instance
        gpg = gnupg.GPG(gnupghome=gpg_dir, keyring=PUBKEYRING, secret_keyring=SECKEYRING)

        if fingerprint:
            # Checks if the GPG directory has private keys and if the entered fingerprint exists
            __check_fingerprint()

        elif keys:
            # Imports the keys from a file
            __import_keys()

        # Asks the user for the password of the private key
        __request_password()

        # Decrypts the file using the fingerprint or key file method
        __decrypt_file()

        # Compares the hash code of the decrypted file with the one entered by the user
        __compare_hash()

    except Exception as exception:
        print(Fore.RED + "✖ Exception in the main() function: " + str(exception.message.lower()) + ".")
        # Prints the traceback
        traceback.print_exc()
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "   ✖ Exception: KeyboardInterrupt. Please, do not interrupt the execution.\n"
              + Fore.RESET)
        sys.exit(1)


########################################
#             MAIN PROGRAM             #
########################################
if __name__ == '__main__':

    check_root()                    # Function to check the type of user
    arguments = menu.check_menu()   # Checks the options entered by the user when running the script
    main(arguments)                 # Main function
