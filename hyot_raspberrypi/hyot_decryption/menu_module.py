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
#           FILE:     menu_module.py                                                                                   #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module parses the menu                                                                      #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded by the main script: hyot_decryption.py                                         #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     02/06/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module parses the menu"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import traceback                                # Print or retrieve a stack traceback
    import argparse                                 # Python command-line parsing library
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in menu_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#               FUNCTIONS              #
########################################
def check_menu():
    """Checks the options entered by the user when running the script
    :return: args Values of the arguments entered by the user in the console
    """

    try:

        # Creates a parser
        parser = argparse.ArgumentParser(
            description=Style.BRIGHT + "HYOT DECRYPTION/HELP: " + Style.RESET_ALL + "This script allow to decrypt a file "
                                       "previously encrypted with GPG", add_help=False)

        # Groups
        general_group = parser.add_argument_group('General options')

        # ### General group ###
        # Help option
        general_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                                   help='Shows the help.')

        # Directory where the public and private key rings and the trust database of GPG are located
        general_group.add_argument("-g", "--gpghome",
                                   required=True, action="store", dest="GPGHOME",
                                   help="Directory where the public and private key rings and the trust database of "
                                        "GPG are located.")

        # Fingerprint of the private key to use
        general_group.add_argument("-f", "--fingerprint",
                                   required=False, action="store", dest="FINGERPRINT",
                                   help="Fingerprint of the private key to use (optional).")

        # Path of the file which stores the public and private key
        general_group.add_argument("-k", "--keys",
                                   required=False, action="store", dest="KEYS",
                                   help="Path of the file which stores the public and private key (optional).")

        # Path of the encrypted file with GPG
        general_group.add_argument("-e", "--encryptedfile",
                                   required=True, action="store", dest="ENCRYPTEDFILE",
                                   help="Path of the encrypted file with GPG.")

        # Directory where the decrypted file will be store
        general_group.add_argument("-d", "--decryptedhome",
                                   required=False, action="store", dest="DECRYPTEDHOME",
                                   help="Directory where the decrypted file will be store (optional). Default: same "
                                        "directory that the encrypted file.")

        # Parses the arguments returning the data from the options specified
        args = parser.parse_args()

        if not args.KEYS and not args.FINGERPRINT:
            print(Fore.RED + "Please, enter some method to indicate the private key. Option: -h/--help to show "
                             "the help." + Fore.RESET)
            sys.exit(0)
        elif args.KEYS and args.FINGERPRINT:
            print(Fore.RED + "Please, enter only one method (by means of fingerprint or file) to indicate the private"
                             " key." + Fore.RESET)
            sys.exit(0)

        return args

    except Exception as argparseError:
        print(Fore.RED + "\nException in the check_menu() function: " + str(argparseError.message.lower()) + ".")
        traceback.print_exc()                       # Prints the traceback
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\r" + Fore.RED + "Exception: KeyboardInterrupt. Please, do not interrupt the execution." + Fore.RESET)
        sys.exit(1)
