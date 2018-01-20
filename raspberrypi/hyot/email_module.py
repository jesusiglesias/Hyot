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
#           FILE:     email_module.py                                                                                  #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to send an email like an alarm notification                       #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Network connection                                                                               #
#          NOTES:     It must be loaded by the main script: raspberrypi_hyot.py                                        #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                         #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     0.1                                                                                              #
#        CREATED:     01/20/17                                                                                         #
#       REVISION:     ---                                                                                              #
# =====================================================================================================================#

"""This module contains the logic to send an email like an alarm notification"""

########################################
#               IMPORTS                #
########################################

try:
    import sys                                          # System-specific parameters and functions
    import time                                         # Time access and conversions
    import smtplib                                      # SMTP protocol client
    from colorama import Fore, Style                    # Cross-platform colored terminal text
    from email.mime.text import MIMEText                # Creating email and MIME objects from scratch

except ImportError as importError:
    print("Error to import: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
FROM = "hyot.project@gmail.com"                                             # Sender's email address
PASSWORD = "hyot2018"                                                       # Sender's password
SERVERIP = "smtp.gmail.com"                                                 # Host/IP of the mail server
SERVERPORT = 587                                                            # Port of the mail server


########################################
#           GLOBAL VARIABLES           #
########################################
session = None                                                              # Mail session


########################################
#               FUNCTIONS              #
########################################
def init():
    """Initializes the mail session"""

    global session

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing the mail session with the email address: "
          + Style.RESET_ALL + FROM)

    try:

        session = smtplib.SMTP(SERVERIP, SERVERPORT)          # Creates a new session of the mail server
        session.ehlo()                                        # Identifies yourself to an ESMTP server
        session.starttls()                                    # Security function, needed to connect to the Gmail server
        session.ehlo()
        session.login(FROM, PASSWORD)                         # Login

        print(Fore.GREEN + "        Mail session initialized correctly" + Fore.RESET)

    except Exception as mailError:
        print(Fore.RED + "        Error to initialize the mail session. Check the mail address, the server connection"
                         " or the network connection. Exception: " + Fore.RESET + str(mailError))
        sys.exit(1)

    time.sleep(1)
    print("\n        ------------------------------------------------------")


def disconnect():
    """Disconnects the mail session"""

    global session

    if not (session is None):
        print("        Disconnecting the mail session")

        # Ends the mail session
        session.quit()

        print(Fore.GREEN + "        Mail session ends successfully" + Fore.RESET)


