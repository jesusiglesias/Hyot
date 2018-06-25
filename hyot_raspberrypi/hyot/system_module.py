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
#           FILE:     system_module.py                                                                                 #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module performs functions with directories and files of the local operating system          #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     01/13/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module performs functions with directories and files of the local operating system"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import email_module as email                    # Module to send emails
    import os                                       # Miscellaneous operating system interfaces
    import shutil                                   # High-level file operations
    import time                                     # Time access and conversions
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in system_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
TEMPFILES_DIR = "tempfiles"                                              # Name of the temporary directory
LOGFILE_DIR = "logs"                                                     # Name of the directory of the log file
LOGFILE = "hyot.log"                                                     # Name of the log file
STEP_CHECKFILE = "Check the existence of the video in the local system"  # Name of the step where the error has occurred


########################################
#           GLOBAL VARIABLES           #
########################################
tempfiles_path = None                                                    # Full path of the temporary local directory


########################################
#               FUNCTIONS              #
########################################
def __logfile_permissions(logfile):
    """
    Sets the permissions for the logger file.

    :param logfile: Path of the log file.
    """

    try:
        os.chmod(logfile, 0700)

    except Exception as permissionsError:
        print(Fore.RED + "✖ Error to set the permissions to the log file. Exception: " + str(permissionsError) + "."
              + Fore.RESET)
        sys.exit(1)


def __create_logger_file(logfile):
    """
    Creates the log file if this one does not exist.

    :param logfile: Path of the log file.
    """

    try:
        open(logfile, "w+")

    except Exception as loggerFileException:
        print(Fore.RED + "✖ Error to create the log file. Exception: " + str(loggerFileException) + "." + Fore.RESET)
        sys.exit(1)

    __logfile_permissions(logfile)                              # Sets the permissions


def create_logger_dir():
    """
    Creates the directory where the log file will be stored.

    :return: log_path Full path of the logger file.
    """

    global LOGFILE_DIR, LOGFILE

    # Path that contains the log file ([project_path]/hyot/logs)
    log_path = os.path.dirname(os.path.abspath(__file__)) + "/" + LOGFILE_DIR

    # Checks if the directory already exists
    if not os.path.exists(log_path):

        try:
            os.makedirs(log_path)                               # Creates the directory

            time.sleep(0.5)

            # After creating, checks again if it was created
            if not os.path.exists(log_path):                    # Directory was not created
                print(Fore.RED + "✖ Error to create the directory: " + log_path + "." + Fore.RESET)
                sys.exit(0)
            else:
                __create_logger_file(log_path + "/" + LOGFILE)  # Creates the log file
                return log_path + "/" + LOGFILE

        except Exception as loggerDirError:
            print(Fore.RED + "✖ Error to create the logger directory. Exception: " + str(loggerDirError) + "."
                  + Fore.RESET)
            sys.exit(1)

    else:
        __create_logger_file(log_path + "/" + LOGFILE)          # Creates the log file
        return log_path + "/" + LOGFILE


def create_localdir():
    """
    Creates the temporary local directory where the videos taken by the Picamera will be stored.
    """

    global TEMPFILES_DIR, tempfiles_path

    print(Style.BRIGHT + Fore.BLACK + "\n      - Initializing the temporary local directory to store the videos "
          "taken by the Picamera" + Style.RESET_ALL),

    # Path that contains the temporary files ([project_path]/hyot/tempfiles)
    tempfiles_path = os.path.dirname(os.path.abspath(__file__)) + "/" + TEMPFILES_DIR

    # Checks if the directory already exists
    if not os.path.exists(tempfiles_path):

        try:
            os.makedirs(tempfiles_path)                         # Creates the directory

            time.sleep(0.5)

            # After creating, checks again if it was created
            if os.path.exists(tempfiles_path):                  # Directory was created
                print(Fore.GREEN + " ✓" + Fore.RESET)
                print("        Directory created successfully: " + tempfiles_path)

            else:                                               # Directory was not created
                print(Fore.RED + " ✖")
                print("        Error to create the directory: " + tempfiles_path + Fore.RESET)
                sys.exit(0)

        except Exception as localDirError:
            print(Fore.RED + " ✖ Error to create the local directory. Exception: " + str(localDirError) + "."
                  + Fore.RESET)
            sys.exit(1)

    else:
        print(Fore.GREEN + " ✓")
        print(Fore.CYAN + "        Directory already exists: " + tempfiles_path + Fore.RESET)

    time.sleep(1)

    print("\n        ------------------------------------------------------")


def remove_localdir():
    """
    Removes the temporary local directory.
    """

    global tempfiles_path

    if not (tempfiles_path is None):

        print("      Removing the temporary local directory: " + tempfiles_path),

        time.sleep(0.25)

        # Checks if the directory exists
        if os.path.exists(tempfiles_path):

            try:
                # Deletes an entire directory tree
                shutil.rmtree(tempfiles_path, ignore_errors=False)

                # After deletion, checks again if it was removed
                if not os.path.exists(tempfiles_path):                  # Directory was removed

                    print(Fore.GREEN + " ✓" + Fore.RESET)

                else:                                                   # Directory was not removed
                    print(Fore.RED + " ✖ Directory was not removed" + Fore.RESET)

            except Exception as removeLocalDirError:
                print(Fore.RED + " ✖ Error to remove the local directory. Exception: " + str(removeLocalDirError) + "."
                      + Fore.RESET)

        else:
            print(Fore.GREEN + " ✓" + Fore.CYAN + " Directory does not exist. Not deleted" + Fore.RESET)

        time.sleep(0.25)


def check_file(localfile, mailto):
    """
    Checks if the file (video) exists in the local system.

    :param localfile: Local path and name of the file to upload to the Cloud (e.g. Dropbox).
    :param mailto: Email address where to send the error notification if it occurs.
    """

    global STEP_CHECKFILE

    if not os.path.exists(localfile):
        print(Fore.RED + "     ✖ File not found in the local system. Exception: " + str(localfile) + ".\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert procedure
        email.print_error_notification_or_send_email(mailto, STEP_CHECKFILE)

        sys.exit(0)  # TODO Logger


def remove_file(localfile, encrypted):
    """
    Removes in the local system the temporary video taken by the Picamera.

    :param localfile: Local path and name of the file to remove.
    :param encrypted: True, to indicate that the encrypted file will be removed. False, to indicate the original video.
    """

    if encrypted:
        print(Fore.LIGHTBLACK_EX + "     -- Removing the encrypted file: " + localfile + Fore.RESET),
    else:
        print(Fore.LIGHTBLACK_EX + "     -- Removing the temporary local file: " + localfile + Fore.RESET),

    time.sleep(1)

    # Checks if the file exists
    if os.path.exists(localfile):

        try:
            # Deletes the file
            os.remove(localfile)

            # After deletion, checks again if it was removed
            if not os.path.exists(localfile):                  # File was removed
                print(Fore.GREEN + " ✓" + Fore.RESET)
            else:                                              # File was not removed
                print(Fore.RED + " ✖ Error to remove the file" + Fore.RESET)

        except Exception as removeFileError:
            print(Fore.RED + " ✖ Error to remove the file. Exception: " + str(removeFileError) + "." + Fore.RESET)

    else:
        print(Fore.GREEN + " ✓" + Fore.CYAN + " File does not exist. Not deleted" + Fore.RESET)
