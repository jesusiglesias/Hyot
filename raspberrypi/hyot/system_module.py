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
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#               FUNCTIONS              #
########################################
def check_file(localfile):
    """Checks if the file exists in the local system
    :param localfile: Local path and name of the file to upload to Dropbox
    """
    # TODO - Exit?
    if not os.path.exists(localfile):
        print(Fore.RED + localfile + " file not found in the local system. Alert is not stored" + Fore.RESET)
        sys.exit(1)
