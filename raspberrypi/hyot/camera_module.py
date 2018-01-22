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
#           FILE:     camera_module.py                                                                                 #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to handle the Picamera                                            #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Connected devices: Picamera                                                                      #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/22/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic to handle the Picamera"""

########################################
#               IMPORTS                #
########################################

try:
    import sys                                          # System-specific parameters and functions
    import time                                         # Time access and conversions
    import picamera                                     # Interface for the Raspberry Pi camera module
    from colorama import Fore, Style                    # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in camera_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
camera = None                                           # Instance of the Picamera


########################################
#               FUNCTIONS              #
########################################
def init():
    """Initializes the Picamera"""

    global camera

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing the Picamera " + Style.RESET_ALL)

    try:
        camera = picamera.PiCamera()                    # Creates an instance of the Picamera

        print(Fore.GREEN + "        Picamera initialized correctly" + Fore.RESET)

    except Exception as cameraError:
        print(Fore.RED + "        Error to initialize the Picamera. Exception: " + Fore.RESET + str(cameraError))
        sys.exit(1)

    time.sleep(1)
    print("\n        ------------------------------------------------------")


def disconnect():
    """Disconnects the Picamera"""

    global camera

    if not (camera is None):
        print("        Disconnecting the Picamera"),

        time.sleep(0.25)

        try:
            camera.close()                              # Closes the Picamera
            camera = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
