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
#           FILE:     menu_module.py                                                                                   #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module parses the menu and checks the options entered by the user                           #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded by the main decryption script: hyot_decryption.py                              #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     02/06/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module parses the menu and checks the options entered by the user"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import argparse                                 # Python command-line parsing library
    import traceback                                # Print or retrieve a stack traceback
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
    """
    Checks the options entered by the user when running the script.

    :returns: args Values of the arguments entered by the user in the console.
    """

    try:

        # Creates a parser
        parser = argparse.ArgumentParser(description=Style.BRIGHT + "HYOT DECRYPTION/HELP: " + Style.RESET_ALL +
                                         "This component allows to decrypt an evidence previously encrypted with GPG,"
                                         " verify the sign and the integrity of the content.",
                                         add_help=False)

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

        # Local path of the encrypted and signed evidence with GPG
        general_group.add_argument("-e", "--encryptedfile",
                                   required=False, action="store", dest="ENCRYPTEDFILE",
                                   help="Local path of the encrypted and signed evidence with GPG (optional).")

        # Link where the encrypted and signed evidence is stored in the cloud
        general_group.add_argument("-l", "--link",
                                   required=False, action="store", dest="LINK",
                                   help="Link where the encrypted and signed evidence is stored in the Cloud"
                                        " (optional).")

        # Hash code of the content of the original evidence
        general_group.add_argument("-ha", "--hash",
                                   required=True, action="store", dest="HASHFILE",
                                   help="Hash code of the content of the original evidence (decrypted).")

        # Fingerprint of the pair of keys to use
        general_group.add_argument("-f", "--fingerprint",
                                   required=False, action="store", dest="FINGERPRINT",
                                   help="Fingerprint of the pair of keys to use (optional).")

        # Path of the file which stores the public and private key
        general_group.add_argument("-k", "--keys",
                                   required=False, action="store", dest="KEYS",
                                   help="Path of the file which stores the public and private key (optional).")

        # Directory where the decrypted evidence will be store
        general_group.add_argument("-d", "--decryptedhome",
                                   required=False, action="store", dest="DECRYPTEDHOME",
                                   help="Directory where the decrypted evidence will be store (optional). Default:"
                                        " same directory that the encrypted evidence when -e/--encryptedfile option is "
                                        "introduced.")

        # Parses the arguments returning the data from the options specified
        args = parser.parse_args()

        # Checks the '--encryptedfile' and '--link' arguments
        if not args.ENCRYPTEDFILE and not args.LINK:
            print(Fore.RED + "✖ Please, enter some method to indicate the evidence to use or type the -h/--help option"
                             " to get more information." + Fore.RESET)
            sys.exit(0)
        elif args.ENCRYPTEDFILE and args.LINK:
            print(Fore.RED + "✖ Please, enter only one way to indicate the evidence to use (local file or link) or"
                             " type the -h/--help option to get more information." + Fore.RESET)
            sys.exit(0)

        # Checks the '--keys' and '--fingerprint' arguments
        if not args.KEYS and not args.FINGERPRINT:
            print(Fore.RED + "✖ Please, enter some method to indicate the pair of keys to use or type the -h/--help"
                             " option to get more information." + Fore.RESET)
            sys.exit(0)
        elif args.KEYS and args.FINGERPRINT:
            print(Fore.RED + "✖ Please, enter only one method (by means of fingerprint or file) to indicate the pair"
                             " of keys to use or type the -h/--help option to get more information." + Fore.RESET)
            sys.exit(0)

        return args

    except Exception as argparseError:
        print(Fore.RED + "\n✖ Exception in the check_menu() function: " + str(argparseError.message.lower()) + ".")
        # Prints the traceback
        traceback.print_exc()
        print(Fore.RESET)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\r" + Fore.RED + "   ✖ Exception: KeyboardInterrupt. Please, do not interrupt the execution.\n"
              + Fore.RESET)
        sys.exit(1)
