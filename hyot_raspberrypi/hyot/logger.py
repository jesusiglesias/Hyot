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
#           FILE:     logger.py                                                                                        #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This class redirects stdout to both file and console                                             #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     06/21/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This class redirects stdout to both file and console"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                          # System-specific parameters and functions
    from colorama import Fore, Style                    # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in logger_class: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#                CLASS                 #
########################################
class Singleton(type):
    """
    Singleton pattern using metaclass.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object):
    """
    Redirects stdout to both file and console.
    """

    __metaclass__ = Singleton

    terminal = None
    logfile = None

    def __init__(self, filename):
        """
        Constructor.
        """

        self.terminal = sys.stdout                      # Console
        self.logfile = open(filename, "w+")             # Log file

    def write(self, message):
        """
        Prints the message by console and save it in the log file.

        :param message: Message shown by console and saved in the log file.
        """

        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        """
        This flush method is needed for python 3 compatibility. This handles the flush command by doing nothing.
        """

        pass


def start(filename):
    """
    Starts the logger, appending the print output to given filename.

    :param filename: Name of the log file.
    """

    sys.stdout = Logger(filename)


def stop():
    """
    Stops the logger and returns print functionality to normal.
    """

    sys.stdout.logfile.close()
    sys.stdout = sys.stdout.terminal
