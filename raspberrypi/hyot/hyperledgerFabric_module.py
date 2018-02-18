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
#           FILE:     hyperledgerFabric_module.py                                                                      #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to make use of Hyperledger Fabric and Blockchain                  #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     TODO                                                                                             #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     02/18/18                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic to make use of Hyperledger Fabric and Blockchain"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                      # System-specific parameters and functions
    import time                                     # Time access and conversions
    import hashlib                                  # Secure hashes and message digests
    import sha3                                     # SHA-3 wrapper (Keccak) for Python
    from colorama import Fore, Style                # Cross-platform colored terminal text

except ImportError as importError:
    print("Error to import in hyperledgerFabric_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
BLOCKSIZE = 65536                                   # Block size (64kb) to hash


########################################
#               FUNCTIONS              #
########################################
def file_hash(video):
    """Applies a hash function to the content of the file
    :param video: File to hash
    """

    try:
        print(Fore.LIGHTBLACK_EX + "   -- Applying a hash function to the content of the video" + Fore.RESET),

        time.sleep(1)

        # Variables
        hasher = hashlib.sha3_512()

        # Opens the file in read and binary mode
        with open(video, 'rb', buffering=0) as f:

            # Reads chunks of a certain size (64kb) to avoid memory failures when not knowing the size of the file
            for b in iter(lambda: f.read(BLOCKSIZE), b''):
                hasher.update(b)                    # Updates the hash

        print(Fore.GREEN + " ✓" + Fore.RESET)

        print(hasher.hexdigest())  # TODO

        time.sleep(1)

    except Exception as hashError:

        print(Fore.RED + " ✕ Error to apply the hash function to the video: " + str(hashError) + Fore.RESET)
        sys.exit(1)  # TODO
