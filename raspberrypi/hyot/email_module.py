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
#    DESCRIPTION:     This module contains the logic to send an email like an alert notification                       #
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

"""This module contains the logic to send an email like an alert notification"""

########################################
#               IMPORTS                #
########################################

try:
    import sys                                          # System-specific parameters and functions
    import time                                         # Time access and conversions
    import smtplib                                      # SMTP protocol client
    from colorama import Fore, Style                    # Cross-platform colored terminal text
    from string import Template                         # Common string operations
    from email.MIMEBase import MIMEBase                 # Email and MIME handling package
    from email.MIMEMultipart import MIMEMultipart       # Create MIME messages that are multipart
    from email.MIMEText import MIMEText                 # Create MIME objects of major type text
    from email import encoders                          # Encoders

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
# Message template for the email TODO - Event that triggers the alert, meters
TEMPLATE = Template("""\
    <html>
        <head></head>
        <body>
            <h3 style="text-align:center">HYOT - ALERT NOTIFICATION</h3>
            <br>
            <p>An alert has been triggered by ${SENSOR} sensor at ${DATETIME} with ID: ${ID}. Below is the full 
            information of the measurement: </p>
        
            <ul>
                <li><b>DHT11 sensor: </b>
                    <ul>
                        <li>Temperature: ${TEMPERATURE} &deg;C</li>
                        <li>Humidity: ${HUMIDITY} &#37;</li>
                    </ul>
                </li>
                <br>
                <li><b>HC-SR04 sensor: </b>
                    <ul>
                        <li>Distance: ${DISTANCE} meters</li>
                    </ul>
                </li>
            </ul>
        
            <p>File uploaded to Dropbox: <a href="${LINK}">link</a>.</p>
        </body>
    </html>
  """)


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


def send_email(mailto, filepath, filename, sensor, timestamp, id, temperature, humidity, distance, link_dropbox):
    """Sends an email to the recipient to notify a triggered alert
    :param mailto: Recipient's email address
    :param filepath: Path of the file to attach
    :param filename: Name of the file to attach
    :param sensor: Sensor that triggers the alert
    :param timestamp: Datetime of the alert
    :param id: Value of this parameter in the measurement
    :param temperature: Value of this parameter in the measurement
    :param humidity: Value of this parameter in the measurement
    :param distance: Value of this parameter in the measurement
    :param link_dropbox: Link to Dropbox where the file is uploaded
    :return: True/False depending on whether the notification was sent
    """

    global session

    # Variables
    subject = "HYOT - Alert notification: {0:s} sensor | {1:s}".format(sensor, timestamp)    # Subject of the email
    # Message of the email in HTML format
    message = TEMPLATE.substitute(SENSOR=sensor, DATETIME=timestamp, ID=id, TEMPERATURE=temperature, HUMIDITY=humidity, DISTANCE=distance, LINK=link_dropbox)

    print(Fore.LIGHTBLACK_EX + "  -- Sending alert notification to the following email address: " + mailto + Fore.RESET),
    time.sleep(1)

    # Creates an instance of MIMEMultipart
    email_instance = MIMEMultipart()

    # Constructs the email
    email_instance["From"] = FROM                               # Sender's email address
    email_instance["To"] = mailto                               # Recipient's email address
    email_instance["Subject"] = subject

    # Creates and attaches the message in HTML text
    email_instance.attach(MIMEText(message, 'html'))

    try:
        # Opens the file to attach
        attachment = open(filepath, "rb")

        # Creates an instance of MIMEBase
        part = MIMEBase('application', 'octet-stream')

        # Steps to convert the file into a Base64
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Closes the open file
        attachment.close()

        # Attaches the file
        email_instance.attach(part)

    except IOError:                                              # Error to open the file
        print(Fore.CYAN + " Could not open the file so it is not attached to the email" + Fore.RESET),

    try:
        # Send the message via a SMTP server
        session.sendmail(FROM, mailto, email_instance.as_string())

        print(Fore.GREEN + " ✓" + Fore.RESET)
        return True

    except Exception as error:
        print(Fore.RED + " ✕ Error sending the email: " + str(error) + Fore.RESET)
        return False


def disconnect():
    """Disconnects the mail session"""

    global session

    if not (session is None):
        print("        Disconnecting the mail session"),

        time.sleep(0.25)

        try:
            # Ends the mail session
            session.quit()
            session = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
