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
#           FILE:     hyot_decryption.py                                                                               #
#                                                                                                                      #
#          USAGE:     sudo python hyot_decryption.py                                                                   #
#                                                                                                                      #
#    DESCRIPTION:     This script decrypts a file previously encrypted with GPG                                        #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Root user, Have access to a compatible version of the GnuPG executable,                          #
#                     Encrypted file with GPG                                                                          #
#          NOTES:     ---                                                                                              #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     02/06/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This script decrypts a file previously encrypted with GPG"""

########################################
#               IMPORTS                #
########################################
try:
    import getpass                                  # Portable password input
    import gnupg                                    # GnuPG’s key management, encryption and signature functionality
    import os                                       # Miscellaneous operating system interfaces
    import sys                                      # System-specific parameters and functions
    import time                                     # Time access and conversions
    import traceback                                # Print or retrieve a stack traceback
    from colorama import Fore, Style                # Cross-platform colored terminal text
    from pyfiglet import Figlet                     # Text banners in a variety of typefaces

    import hyot_decryption.menu_module as menu      # Module to execute initial checks and to parse the menu

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
decrypted_dir = None                                # Directory where the decrypted file will be store
output_file = None                                  # Full path (path + filename) where the decrypted file will be store


########################################
#               FUNCTIONS              #
########################################
def check_root():
    """Checks that the script is run with a root user"""

    if not os.geteuid() == 0:
        print(Fore.RED + "You need to have root privileges to run this script. Please try it again using 'sudo'."
              + Fore.RESET)
        sys.exit(0)


def header():
    """Prints the header in the console"""

    figlet = Figlet(font='future_8', justify='center')      # Figlet

    # Header
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + figlet.renderText("HYOT DECRYPT"))
    print("This script allows to decrypt a file previously encrypted with GPG.\n" + Style.RESET_ALL)

    time.sleep(1)                                           # Wait time - 1 second


def check_existence():
    """Checks if the GPG directory, the file with the private and public key, the encrypted file and the directory,
    where the decrypted file will be store, exist in the local system"""

    global gpg_dir, keys, encrypted_file, decrypted_dir

    # Checks if the GPG directory exists
    if not os.path.isdir(gpg_dir):
        print(Fore.RED + "   The entered GPG directory does not exist or is not a directory in the local system."
              + Fore.RESET)
        sys.exit(0)

    # Checks if the file, which must contain the public and private key, exists
    if keys:
        if not os.path.isfile(keys):
            print(Fore.RED + "   The entered key file does not exist or is not a file in the local system."
                  + Fore.RESET)
            sys.exit(0)

    # Checks if the encrypted file exists
    if not os.path.isfile(encrypted_file):
        print(Fore.RED + "   The encrypted file does not exist or is not a file in the local system." + Fore.RESET)
        sys.exit(0)

    # Checks if the directory, where the decrypted file will be store, exists
    if not os.path.isdir(decrypted_dir):
        print(Fore.RED + "   The directory, where the decrypted file will be store, does not exist or is not a "
                         "directory in the local system." + Fore.RESET)
        sys.exit(0)


def check_extension():
    """Checks if the encrypted file has the right extension"""

    global EXT, encrypted_file

    # Obtains the extension
    ext = os.path.splitext(encrypted_file)[-1].lower()

    if ext != EXT:
        print(Fore.RED + "   The encrypted file has an extension that it is not allowed. It must be a file with "
                         "format: .gpg." + Fore.RESET)
        sys.exit(0)


def request_password():
    """Asks the user for the password of the private key"""

    global password

    # Asks the user for the password of the private key
    password = getpass.getpass(Fore.BLUE + "   Enter the password for the private key: " + Fore.RESET) or None

    # Checks if the password is empty
    if password is None or password.isspace():
        print(Fore.RED + "   The password can not be empty." + Fore.RESET)
        sys.exit(0)

    # Removes the spaces
    password = password.replace(" ", "")


def check_fingerprint():
    """Checks if the GPG directory has private keys and if the entered fingerprint exists"""

    global gpg, fingerprint, fingerprint_array

    # Obtains the private keys
    private_keys = gpg.list_keys(True)

    # Checks if the GPG directory has private keys
    if len(private_keys) == 0:
        print(Fore.RED + "   The GPG directory does not contain any private key. Please, import the private key to "
                         "decrypt the file (option: -k/--keys)." + Fore.RESET)
        sys.exit(0)

    # Obtains the fingerprint of each private key
    for key in private_keys:
        fingerprint_array.append(key['fingerprint'])

    # Checks if the entered fingerprint exists in the key ring
    if fingerprint not in fingerprint_array:
        print(Fore.RED + "   The entered fingerprint does not exist in the indicated GPG directory. Please, import the "
                         "private key to decrypt the file or use another fingerprint." + Fore.RESET)
        sys.exit(0)


def decrypt_file():
    """Decrypts the file using the entered fingerprint or the imported key from a file"""

    global gpg, password, encrypted_file, output_file

    with open(encrypted_file, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=password, output=output_file)

        if not status.ok:
            print(Fore.RED + "\n   The decryption has failed. Main reasons: " + Fore.RESET)
            print(Fore.RED + "     - File was encrypted with another RSA key." + Fore.RESET)
            print(Fore.RED + "     - Bad passphrase to unlock the GPG secret key." + Fore.RESET)
            print(Fore.RED + "     - No valid OpenPGP data found." + Fore.RESET)
            print(Fore.RED + "     - Output is a directory." + Fore.RESET)
        else:
            print(Fore.GREEN + "\n   File decrypts successfully in the path: " + output_file + "." + Fore.RESET)


def import_keys():
    """Import the public and private key from a file"""

    global gpg, keys

    keys_data = open(keys, 'rb').read()
    import_result = gpg.import_keys(keys_data)

    if import_result.count != 2:
        print(Fore.RED + "   The entered key file does not contain two keys (public and private key). Please, use the "
                         "generated file during encryption." + Fore.RESET)
        sys.exit(0)


def main(user_args):
    """Main function
    :param user_args: Values of the options entered by the user
    """

    global PUBKEYRING, SECKEYRING, gpg, gpg_dir, fingerprint, keys, encrypted_file, decrypted_dir, output_file

    # Try-Catch block
    try:

        gpg_dir = user_args.GPGHOME
        fingerprint = user_args.FINGERPRINT
        keys = user_args.KEYS
        encrypted_file = user_args.ENCRYPTEDFILE
        decrypted_dir = user_args.DECRYPTEDHOME

        # Header
        header()

        print(Style.BRIGHT + Fore.BLACK + "-- Initializing the decryption...\n" + Style.RESET_ALL)

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
        check_existence()

        # Checks if the encrypted file has the right extension (.gpg)
        check_extension()

        # Creates the GPG instance
        gpg = gnupg.GPG(gnupghome=gpg_dir, keyring=PUBKEYRING, secret_keyring=SECKEYRING)

        # Decrypts the file using the fingerprint method
        if fingerprint:
            # Checks if the GPG directory has private keys and if the entered fingerprint exists
            check_fingerprint()

            # Asks the user for the password of the private key
            request_password()

            # Decrypts the file using the entered fingerprint
            decrypt_file()

        # Decrypts the file using the key file method
        elif keys:
            # Imports the keys from a file
            import_keys()

            # Asks the user for the password of the private key
            request_password()

            # Decrypts the file
            decrypt_file()

    except Exception as exception:
        print(Fore.RED + "\nException in the main() function: " + str(exception.message.lower()) + ".")
        traceback.print_exc()                       # Prints the traceback
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Exception: KeyboardInterrupt. Please, do not interrupt the execution." + Fore.RESET)
        sys.exit(1)


########################################
#             MAIN PROGRAM             #
########################################
if __name__ == '__main__':

    check_root()                    # Function to check the type of user
    arguments = menu.check_menu()   # Checks the options entered by the user when running the script
    main(arguments)                 # Main function
