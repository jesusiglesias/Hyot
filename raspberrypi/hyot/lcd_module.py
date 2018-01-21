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
#           FILE:     lcd_module.py                                                                                    #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to handle the LCDs                                                #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Connected devices: LCD 16x2 (2)                                                                  #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/21/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic to handle the LCDs"""

########################################
#               IMPORTS                #
########################################
from __future__ import unicode_literals                 # Future statement definitions

try:
    import sys                                          # System-specific parameters and functions
    import time                                         # Time access and conversions
    from colorama import Fore, Style                    # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in lcd_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#           GLOBAL VARIABLES           #
########################################
dht_lcd = None                                          # Instance of the LCD of the DHT11 sensor
hcsr_lcd = None                                         # Instance of the LCD of the HC-SR04 sensor
lcds = []                                               # Stores the instances of all sensors
sensors = []                                            # Stores tne name of all sensors

