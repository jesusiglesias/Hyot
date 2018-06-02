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
#           FILE:     camera_module.py                                                                                 #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to handle the Picamera                                            #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Picamera device connected, Camera interface enabled on the Raspberry Pi                          #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     01/22/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic to handle the Picamera"""

########################################
#               IMPORTS                #
########################################
try:
    import picamera                                     # Interface for the Raspberry Pi camera module
    import sys                                          # System-specific parameters and functions
    import time                                         # Time access and conversions
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
    """
    Initializes the Picamera.
    """

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


def record_video(path, recording_time):
    """
    Record a video for n seconds. Default: 10 seconds.

    :param path: Path where the video will be saved.
    :param recording_time: Time that the recording will take.
    """

    global camera

    try:
        print(Fore.LIGHTBLACK_EX + "   -- Taking a recording of " + str(recording_time) + " seconds and temporarily"
              " storing it in the path: " + path + Fore.RESET),

        time.sleep(1)

        camera.start_recording(path)
        # Pause the recording for n seconds (default value: 10 seconds) and it continually check for recording errors
        camera.wait_recording(recording_time)
        camera.stop_recording()

        print(Fore.GREEN + " ✓" + Fore.RESET)

        time.sleep(1)

    except Exception as recordError:

        print(Fore.RED + " ✕ Error to record the video: " + str(recordError) + Fore.RESET)
        sys.exit(1)  # TODO


def disconnect():
    """
    Disconnects the Picamera.
    """

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
