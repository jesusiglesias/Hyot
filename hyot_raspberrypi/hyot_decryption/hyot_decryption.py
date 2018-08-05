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
#    DESCRIPTION:     This component decrypts an evidence previously encrypted with GPG, verifies the sign and the     #
#                     integrity of the content                                                                         #
#                                                                                                                      #
#        OPTIONS:     Type '-h' or '--help' option to show the help                                                    #
#   REQUIREMENTS:     Root user, Access to a compatible version of the GnuPG executable, Encrypted and signed evidence #
#                     with GPG or link of the evidence, Valid key or fingerprint and hash, Module: menu_module.py      #
#          NOTES:     ---                                                                                              #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.1.0                                                                                            #
#        CREATED:     25/07/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This component decrypts an evidence previously encrypted with GPG, verifies the sign and the integrity of the
content"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import datetime                                 # Basic date and time types
    import getpass                                  # Portable password input
    import gnupg                                    # GnuPG’s key management, encryption and signature functionality
    import hashlib                                  # Secure hashes and message digests
    import menu_module as menu                      # Module to execute initial checks and to parse the menu
    import os                                       # Miscellaneous operating system interfaces
    import re                                       # Regular expression
    import requests                                 # HTTP for Humans
    import sha3                                     # SHA-3 wrapper (Keccak) for Python
    import socket                                   # Low-level networking interface
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
password = None                                     # Passphrase of the private key
keys = None                                         # Local path of the file which stores the public and private key
fingerprint = None                                  # Fingerprint of the pair of keys to use
fingerprint_array = []                              # Array to store the existing fingerprints
encrypted_file = None                               # Path of the encrypted and signed evidence with GPG
link = None                                         # Link of the evidence uploaded to the Cloud (e.g. Dropbox)
hash_file = None                                    # Hash code of the decrypted evidence
decrypted_dir = None                                # Directory where the decrypted evidence will be store
output_file = None                                  # Full path where the decrypted evidence will be store


########################################
#               FUNCTIONS              #
########################################
def check_root():
    """
    Checks that the component is run with a root user.
    """

    if not os.geteuid() == 0:
        print(Fore.RED + "✖ You need to have root privileges to run this component. Please, try it again using sudo."
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


   A PoC for traceability in IoT environments through Hyperledger Fabric by:

   - Jesús Iglesias García, jesusgiglesias@gmail.com

   -----------------------------------------------------

   HYOT - DECRYPTION

   This component allows to decrypt an evidence previously encrypted with GPG, verify the sign and the
   integrity of the content.
   
   Type the '-h' or '--help' option to get more information.

   """

    # Header
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + banner + Style.RESET_ALL)

    # Wait time - 1 second
    time.sleep(1)


def __check_network():
    """
    Checks if the system is connected to the network.
    """

    # Host: 8.8.8.8 (google-public-dns-a.google.com)
    # OpenPort: 53/tcp
    # Service: domain (DNS/TCP)

    # Variables
    host = "8.8.8.8"
    port = 53
    timeout = 5

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    except socket.error:
        print(Fore.RED + "   ✖ System is not connected to the network. Please, enable the network to continue the"
                         " execution.\n" + Fore.RESET)
        sys.exit(1)


def __url_validator():
    """
    Checks that the entered string is an URL or IP.
    """

    global link

    regex_url = re.compile(
        r'^(?:http|ftp)s?://'                                                                   # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'    # Domain
        r'localhost|'                                                                           # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                                                  # IP
        r'(?::\d+)?'                                                                            # Optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not re.match(regex_url, link):
        print(Fore.RED + "   ✖ The link entered has not URL or IP format. Please, type a valid URL to download the"
                         " encrypted and signed evidence.\n" + Fore.RESET)
        sys.exit(0)


def __download_file():
    """
    Downloads the file from the Cloud.
    """

    global link

    # Checks if the system is connected to the network
    __check_network()

    # Checks that the entered string is an URL
    __url_validator()

    print(Style.BRIGHT + Fore.BLACK + "      - Downloading encrypted and signed evidence" + Style.RESET_ALL),

    split_link = link.split("/")[-1].split("?")

    # Checks a substring of the Dropbox link, where:
    # ?dl=0 will show the file in the preview page
    # ?dl=1 will force the file to download
    if split_link[1] == "dl=0":
        link = link.replace("?dl=0", "?dl=1")

    # Obtains the name of the evidence (Dropbox format)
    filename = split_link[0]
    fullpath = os.path.dirname(os.path.abspath(__file__)) + "/" + filename

    try:
        response = requests.get(link)                       # Downloads the evidence
    except requests.exceptions.RequestException as downloadEvidence:
        print(Fore.RED + " ✕")
        print("\n      ✖ Error to download the evidence. Error: " + str(downloadEvidence) + ".\n" + Fore.RESET)
        sys.exit(1)

    try:
        with open(fullpath, "wb") as code:                  # Saves the evidence in a local file
            for chunk in response.iter_content():
                code.write(chunk)

        del response

        print(Fore.GREEN + " ✓\n" + Fore.RESET)
        return fullpath
    except Exception as fileException:
        print(Fore.RED + " ✕")
        print("\n      ✖ Error to save the evidence downloaded. Error: " + str(fileException) + ".\n" + Fore.RESET)
        sys.exit(1)


def __check_existence():
    """
    Checks if the GPG directory, the file with the private and public key, the encrypted and signed evidence and the
    directory where the decrypted evidence will be store exist in the local system.
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

    # Checks if the encrypted and signed evidence exists
    if not os.path.isfile(encrypted_file):
        print(Fore.RED + "   ✖ The encrypted and signed evidence does not exist or is not a file in the local"
                         " system.\n" + Fore.RESET)
        sys.exit(0)

    # Checks if the directory, where the decrypted evidence will be store, exists
    if decrypted_dir:
        if not os.path.isdir(decrypted_dir):
            print(Fore.RED + "   ✖ The directory, where the decrypted evidence will be store, does not exist or is not"
                             " a directory in the local system.\n" + Fore.RESET)
            sys.exit(0)


def __check_extension():
    """
    Checks if the encrypted and signed evidence has the right extension.
    """

    global EXT, encrypted_file

    # Obtains the extension
    ext = os.path.splitext(encrypted_file)[-1].lower()

    if ext != EXT:
        print(Fore.RED + "   ✖ The encrypted and signed evidence has an extension which is not allowed. It must be a"
                         " file with format: .gpg.\n" + Fore.RESET)
        sys.exit(0)


def __check_fingerprint():
    """
    Checks if the GPG directory has private keys and if the entered fingerprint exists.
    """

    global gpg, fingerprint, fingerprint_array

    # Obtains the public keys
    public_keys = gpg.list_keys(False)

    # Obtains the private keys
    private_keys = gpg.list_keys(True)

    # Checks if the GPG directory has public and private keys (len(public_keys/private_keys) == 0)
    if not public_keys and not private_keys:
        print(Fore.RED + "   ✖ The GPG directory does not contain any public or private key. Please, import the pair of"
                         " keys with the -k/--keys option to continue the process.\n" + Fore.RESET)
        sys.exit(0)

    # Obtains the fingerprint of each private key
    for key in private_keys:
        fingerprint_array.append(key['fingerprint'])

    # Checks if the entered fingerprint exists in the key ring
    if fingerprint not in fingerprint_array:
        print(Fore.RED + "   ✖ The entered fingerprint does not exist in the indicated GPG directory. Please, import "
                         "the pair of keys to continue the process or use an existing fingerprint.\n" +
              Fore.RESET)
        sys.exit(0)


def __import_keys():
    """
    Imports the public and private keys from a file.
    """

    global gpg, keys

    keys_data = open(keys, 'rb').read()
    import_result = gpg.import_keys(keys_data)

    if import_result.count != 2:
        print(Fore.RED + "   ✖ The entered key file does not contain the pair of keys (public and private key). Please,"
                         " use the file generated in the component of monitoring of environmental events.\n" +
              Fore.RESET)
        sys.exit(0)


def __request_password():
    """
    Asks the user for the password of the private key. User has 3 attempts.
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
    Obtains the hash code of the decrypted evidence and compares it with the one entered by the user.

    :return: True, to indicate that the original evidence has not altered -stay unchanged-. False, otherwise.
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
        if hasher.hexdigest() == hash_file:                        # Original evidence has not been altered

            print(Fore.GREEN + " ✓" + Fore.RESET)
            print("\n      Both hash codes are the same. The original evidence has not been altered and its integrity"
                  " is guaranteed.\n")

        else:                                                      # Original evidence has been altered
            print(Fore.YELLOW + " " + u"\u26A0" + Fore.RESET)
            print("\n      Both hash codes are different. The original evidence may have been manipulated by a"
                  " malicious third party and therefore its integrity is not guaranteed.\n")

    except Exception as hashError:

        print(Fore.RED + " ✕")
        print("\n      ✖ Error to calculate the hash code of the original evidence. Error: " + str(hashError) + ".\n"
              + Fore.RESET)


def __verify_signature(verified_data):
    """
    Verifies the signature of the evidence.

    :param verified_data Result of the verification of the signature.
    """

    print(Style.BRIGHT + Fore.BLACK + "\n      - Verifying the signature" + Style.RESET_ALL),

    if verified_data.signature_id is not None:
        print(Fore.GREEN + " ✓" + Fore.RESET)

        print("\n      Information of the signature")
        print("      ----------------------------")
        print("      User identity: " + verified_data.username)
        print("      Signature made: " +
              datetime.datetime.fromtimestamp(int(verified_data.sig_timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
        print("      Fingerprint used: " + verified_data.fingerprint)

        if verified_data.trust_level is not None:

            print("\n      Trust level of the key used")
            print("      ---------------------------")

            if int(verified_data.trust_level) == 0:
                print("      This key is not certified with a trusted signature because it has not been marked as"
                      " reliable or it does not belong to the GPG trust ring.")
            else:
                print("      " + str(verified_data.trust_level) + " - " + str(verified_data.trust_text))
    else:
        print(Fore.YELLOW + " " + u"\u26A0" + Fore.RESET)
        print("\n      Evidence was not signed.")


def __decrypt_file():
    """
    Decrypts the evidence using the entered fingerprint or the imported key from a file.
    """

    global gpg, password, encrypted_file, output_file

    print(Style.BRIGHT + Fore.BLACK + "\n      - Decrypting" + Style.RESET_ALL),

    with open(encrypted_file, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=password, output=output_file)

        if not status.ok:

            print(Fore.RED + " ✕")
            print("\n      The decryption has failed. Main reasons: \n")
            print("       - Evidence was encrypted with another RSA key.")
            print("       - Bad passphrase to unlock the GPG secret key.")
            print("       - No valid OpenPGP data found.")
            print("       - Output is a directory.\n" + Fore.RESET)
            sys.exit(0)
        else:
            print(Fore.GREEN + " ✓" + Fore.RESET)
            print("\n      Evidence successfully decrypted in the path: " + str(output_file) + ".")

            # Verifies the signature
            __verify_signature(status)


def main(user_args):
    """
    Main function.

    :param user_args: Values of the options entered by the user.
    """

    global PUBKEYRING, SECKEYRING, gpg, gpg_dir, fingerprint, keys, encrypted_file, link, hash_file,\
        decrypted_dir, output_file

    # Try-Catch block
    try:

        # Variables
        gpg_dir = user_args.GPGHOME
        fingerprint = user_args.FINGERPRINT
        keys = user_args.KEYS
        encrypted_file = user_args.ENCRYPTEDFILE
        link = user_args.LINK
        hash_file = user_args.HASHFILE
        decrypted_dir = user_args.DECRYPTEDHOME

        # Header
        header()

        print(Style.BRIGHT + Fore.BLACK + "   -- Initializing the decryption...\n" + Style.RESET_ALL)

        time.sleep(1)

        # Link of the evidence to download entered by the user
        if link:
            # Downloads the evidence from the Cloud
            encrypted_file = __download_file()

        # Checks if the directory, which will store the decrypted evidence, has been entered by the user (optional
        # argument)
        if not decrypted_dir:
            # Obtains the directory from the encrypted evidence, removing the filename
            decrypted_dir = "/".join(encrypted_file.split("/")[:-1])

            # Full path where the decrypted evidence will be stored. It removes the extension: .gpg
            output_file = os.path.splitext(encrypted_file)[0]
        else:
            # Full path where the decrypted evidence will be stored. Takes the name of the encrypted and signed evidence
            # removing the extension '.gpg' and adds it to the directory that will store the decrypted evidence
            output_file = "/".join([decrypted_dir, os.path.splitext(encrypted_file.split("/")[-1])[0]])

            output_file = output_file.replace("//", "/")

        # Checks if the entered directories and files exist in the local system
        __check_existence()

        # Checks if the encrypted and signed evidence has the right extension (.gpg)
        __check_extension()

        # Creates the GPG instance
        gpg = gnupg.GPG(gnupghome=gpg_dir, keyring=PUBKEYRING, secret_keyring=SECKEYRING)

        if fingerprint:
            # Checks if the GPG directory has private keys and if the entered fingerprint exists
            __check_fingerprint()

        elif keys:
            # Imports the pair of keys from a file
            __import_keys()

        # Asks the user for the password of the private key
        __request_password()

        # Decrypts the evidence using the fingerprint or key file method
        __decrypt_file()

        # Compares the hash code of the decrypted evidence with the one entered by the user
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
    arguments = menu.check_menu()   # Checks the options entered by the user when running the component
    main(arguments)                 # Main function
