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
#           FILE:     system_module.py                                                                                 #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module performs functions in the local operating system                                     #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/13/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module performs functions in the local operating system"""

########################################
#               IMPORTS                #
########################################

try:
    import sys                                      # System-specific parameters and functions
    import os                                       # Miscellaneous operating system interfaces
    import shutil                                   # High-level file operations
    import time                                     # Time access and conversions
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
TEMPFILES_DIR = "tempfiles"                         # Name of the temporary directory


########################################
#           GLOBAL VARIABLES           #
########################################
tempfiles_path = None                               # Full path of the temporary local directory


########################################
#               FUNCTIONS              #
########################################
def create_localdir():
    """Creates the temporary local directory where the images taken by the Picamera will be stored"""  # TODO

    global tempfiles_path

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Creating the temporary local directory to store the images taken "
          "by the Picamera" + Style.RESET_ALL)  # TODO

    # Path that contains the temporary files ([project_path]/hyot/tempfiles)
    tempfiles_path = os.path.dirname(os.path.abspath(__file__)) + "/" + TEMPFILES_DIR

    # Checks if the directory already exists
    if not os.path.exists(tempfiles_path):

        os.makedirs(tempfiles_path)                 # Creates the directory

        time.sleep(0.5)

        # After creating, checks again if it was created
        if os.path.exists(tempfiles_path):          # Directory was created
            print(Fore.GREEN + "        " + Style.BRIGHT + tempfiles_path + Style.NORMAL + " directory created "
                               "successfully" + Fore.RESET)

        else:                                       # Directory was not created
            print(Fore.RED + "        Error to create the " + Style.BRIGHT + tempfiles_path + Style.NORMAL +
                  " directory" + Fore.RESET)
            sys.exit(1)

    else:
        print(Fore.GREEN + "        " + Style.BRIGHT + tempfiles_path + Style.NORMAL + " directory already exists"
              + Fore.RESET)

    time.sleep(1)

    print("\n        ------------------------------------------------------")


def remove_localdir():
    """Removes the temporary local directory"""

    global tempfiles_path

    if not (tempfiles_path is None):

        print("        Removing the temporary local directory: " + tempfiles_path)

        # Checks if the directory exists
        if os.path.exists(tempfiles_path):

            try:
                # Deletes an entire directory tree
                shutil.rmtree(tempfiles_path, ignore_errors=False)

                # After deletion, checks again if it was removed
                if not os.path.exists(tempfiles_path):                  # Directory was removed
                    print(Fore.GREEN + "        Directory removed successfully" + Fore.RESET)

                else:                                                   # Directory was not removed
                    print(Fore.RED + "        Error to remove the directory" + Fore.RESET)

            except OSError:
                print(Fore.RED + "        Error to remove. No such directory: " + tempfiles_path
                      + Fore.RESET)

        else:
            print(Fore.CYAN + "        Directory does not exist. Not deleted" + Fore.RESET)


def check_file(localfile):
    """Checks if the file exists in the local system
    :param localfile: Local path and name of the file to upload to Dropbox
    """
    # TODO - Exit?
    if not os.path.exists(localfile):
        print(Fore.RED + localfile + " file not found in the local system. Alert is not stored" + Fore.RESET)
        sys.exit(1)


def remove_file(localfile):
    """Removes in the local system the temporary image taken by the Picamera TODO
    :param localfile: Local path and name of the file to remove
    """

    print("Removing the temporary local file: " + localfile)

    # Checks if the file exists
    if os.path.exists(localfile):

        try:
            # Deletes the file
            os.remove(localfile)

            # After deletion, checks again if it was removed
            if not os.path.exists(localfile):                  # File was removed
                print(Fore.GREEN + "File removed successfully" + Fore.RESET)

            else:                                              # File was not removed
                print(Fore.RED + "Error to remove the file" + Fore.RESET)

        except OSError:
            print(Fore.RED + "Error to remove. No such file: " + localfile + Fore.RESET)

    else:
            print(Fore.CYAN + "File does not exist. Not deleted" + Fore.RESET)
