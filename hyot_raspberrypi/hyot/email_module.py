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
#           FILE:     email_module.py                                                                                  #
#                                                                                                                      #
#          USAGE:     ---                                                                                              #
#                                                                                                                      #
#    DESCRIPTION:     This module contains the logic to send emails when an alert notification is triggered or an      #
#                     error occurs during the execution of the measurement procedure                                   #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     Gmail account, Connection to the network                                                         #
#          NOTES:     It must be loaded by the main traceability script: hyot_main.py                                  #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     01/20/18                                                                                         #
#       REVISION:     ---                                                                                              #
#                                                                                                                      #
# =====================================================================================================================#

"""This module contains the logic to send emails when an alert notification is triggered or an error occurs during the
   execution of the measurement procedure"""

########################################
#               IMPORTS                #
########################################
try:
    import sys                                          # System-specific parameters and functions
    import logger as logger                             # Class to redirect stdout to both file and console
    import os                                           # Miscellaneous operating system interfaces
    import smtplib                                      # SMTP protocol client
    import time                                         # Time access and conversions
    import yaml                                         # YAML parser and emitter for Python
    from colorama import Fore, Style                    # Cross-platform colored terminal text
    from email.MIMEBase import MIMEBase                 # Email and MIME handling package
    from email.MIMEMultipart import MIMEMultipart       # Create MIME messages that are multipart
    from email.MIMEText import MIMEText                 # Create MIME objects of major type text
    from email import encoders                          # Encoders
    from string import Template                         # Common string operations

except ImportError as importError:
    print("Error to import in email_module: " + importError.message.lower() + ".")
    sys.exit(1)
except KeyboardInterrupt:
    print("\rException: KeyboardInterrupt. Please, do not interrupt the execution.")
    sys.exit(1)


########################################
#       LOAD YAML CONFIGURATION        #
########################################
conf = None
try:
    conf = yaml.load(open('conf/hyot.yml'))

except IOError as ioERROR:
    print(Fore.RED + "✖ Please, place the configuration file (hyot.yml) inside a directory called 'conf' in the root "
                     "path (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)
except yaml.YAMLError as yamlError:
    print(Fore.RED + "✖ The configuration file (conf/hyot.yml) has not the YAML format." + Fore.RESET)
    sys.exit(1)


########################################
#              CONSTANTS               #
########################################
try:
    FROM = conf['email']['from']                                    # Sender's email address
    PASSWORD = conf['email']['password']                            # Sender's password

except (KeyError, TypeError) as keyError:
    print(Fore.RED + "✖ Please, make sure that the keys: [email|from] and [email|password] exist in the configuration "
                     "file (conf/hyot.yml)." + Fore.RESET)
    sys.exit(1)

SERVERIP = "smtp.gmail.com"                                         # Host/IP of the mail server
SERVERPORT = 587                                                    # Port of the mail server
TEMPLATEPATH = "template/email_template.html"                       # Path of the email template
ERRORTEMPLATEPATH = "template/error_measurement_template.html"      # Path of the error template
LOGFILE_DIR = "logs"                                                # Name of the directory of the log file
LOGFILE = "hyot.log"                                                # Name of the log file
# Names to identify the step where the error has occurred
STEP_ALERTEMAIL_TEMPLATE = "Send email of alert - Template"
STEP_ALERTEMAIL_ATTACHMENT = "Send email of alert - Attachment"
STEP_ALERTEMAIL_SEND = "Send email of alert - Sending"


########################################
#           GLOBAL VARIABLES           #
########################################
session = None                                          # Mail session


########################################
#               FUNCTIONS              #
########################################
def init():
    """
    Initializes the mail session with a Gmail account.
    """

    global FROM, PASSWORD, SERVERIP, SERVERPORT, session

    print("\n      " + Style.BRIGHT + Fore.BLACK + "- Initializing the mail session with the email address: "
          + Style.RESET_ALL + FROM),

    try:
        session = smtplib.SMTP(SERVERIP, SERVERPORT)          # Creates a new session of the mail server
        session.ehlo()                                        # Identifies yourself to an ESMTP server
        session.starttls()                                    # Security function, needed to connect to the Gmail server
        session.ehlo()
        session.login(FROM, PASSWORD)                         # Login

        print(Fore.GREEN + " ✓" + Fore.RESET)

    except Exception as mailError:
        print(Fore.RED + " ✖ Error to initialize the mail session. Check the mail address, the server connection or "
                         "the network connection. Exception: " + str(mailError) + "." + Fore.RESET)
        sys.exit(1)

    time.sleep(1)
    print("\n        ------------------------------------------------------")


def __read_template(filename):
    """
    Reads the email template and generates a Template instance.

    :param filename: File to read.

    :return: Template instance.
    """

    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()

    return Template(template_file_content)


def send_email(mailto, filepath, filename, timestamp, alert_id, temperature, humidity, distance, link,
               alert_origin, threshold_value):
    """
    Sends an email to the recipient to notify a triggered alert.

    :param mailto: Recipient's email address.
    :param filepath: Path of the file to attach.
    :param filename: Name of the file to attach.
    :param timestamp: Datetime of the alert.
    :param alert_id: Identifier of the alert.
    :param temperature: Value of this parameter in the measurement.
    :param humidity: Value of this parameter in the measurement.
    :param distance: Value of this parameter in the measurement.
    :param link: Link of the Cloud (e.g. Dropbox) where the file was uploaded.
    :param alert_origin: Contains the sensor and the event that triggered the alert.
    :param threshold_value: Indicates the value of the event threshold that triggered the alert.
    """

    global TEMPLATEPATH, STEP_ALERTEMAIL_TEMPLATE, STEP_ALERTEMAIL_ATTACHMENT, STEP_ALERTEMAIL_SEND, FROM, session

    # Extracts the sensor and the event
    sensor, event = alert_origin.split('-')
    sensor = sensor.strip()
    event = event.strip()

    # Subject of the email
    subject = "HYOT - Alert notification: {0:s} | {1:s} | {2:s}".format(sensor, event, timestamp)

    print(Fore.LIGHTBLACK_EX + "     -- Sending alert notification to the following email address: " + mailto
          + Fore.RESET),

    # Message of the email in HTML format
    try:
        message = __read_template(os.path.dirname(os.path.abspath(__file__)) + "/" + TEMPLATEPATH).substitute(
            EVENT=event,
            SENSOR=sensor,
            DATETIME=timestamp,
            THRESHOLD=threshold_value,
            ID=alert_id,
            TEMPERATURE=temperature,
            HUMIDITY=humidity,
            DISTANCE=distance,
            LINK=link)

    except Exception as templateError:
        print(Fore.RED + " ✖ Error in the email template. Exception: " + str(templateError) + ".\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        print_error_notification_or_send_email(mailto, STEP_ALERTEMAIL_TEMPLATE)

        sys.exit(1)

    time.sleep(0.5)

    # Creates an instance of MIMEMultipart
    email_instance = MIMEMultipart()

    # Constructs the email
    email_instance["From"] = FROM                             # Sender's email address
    email_instance["To"] = mailto                             # Recipient's email address
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

    except IOError as attachedError:                          # Error to open the file
        print(Fore.RED + " ✖ Could not open the evidence so it is not attached to the email. Exception: " +
              str(attachedError) + ".\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        print_error_notification_or_send_email(mailto, STEP_ALERTEMAIL_ATTACHMENT)

        sys.exit(1)

    try:
        # Sends the message via a SMTP server
        session.sendmail(FROM, mailto, email_instance.as_string())

        print(Fore.GREEN + " ✓" + Fore.RESET)

    except Exception as sendError:
        print(Fore.RED + " ✖ Error to send the email. Exception: " + str(sendError) + ".\n" + Fore.RESET)

        # Prints a message or sends an email when an error occurs during the alert protocol
        print_error_notification_or_send_email(mailto, STEP_ALERTEMAIL_SEND)

        sys.exit(1)


def __send_email_measurement_error(mailto, step):
    """
    Sends an email to the recipient to notify that an execution error has occurred during the measurement.

    :param mailto: Recipient's email address.
    :param step: Step where the error has occurred.
    """

    global ERRORTEMPLATEPATH, FROM, LOGFILE_DIR, LOGFILE, attachError, session

    # Variable
    attachError = None

    print(Fore.CYAN + "     Sending email to the following email address: " + mailto + " to notify the measurement"
                      " error" + Fore.RESET),

    # Subject of the email
    subject = "HYOT - Measurement error - Step: " + step

    # Message of the email in HTML format
    try:
        message = __read_template(os.path.dirname(os.path.abspath(__file__)) + "/" + ERRORTEMPLATEPATH).substitute(
            STEP=step)

    except Exception as templateError:
        print(Fore.RED + " ✖ Error in the email template. Exception: " + str(templateError) + ".\n" + Fore.RESET)
        sys.exit(1)

    time.sleep(0.5)

    # Creates an instance of MIMEMultipart
    email_instance = MIMEMultipart()

    # Constructs the email
    email_instance["From"] = FROM                             # Sender's email address
    email_instance["To"] = mailto                             # Recipient's email address
    email_instance["Subject"] = subject

    # Creates and attaches the message in HTML text
    email_instance.attach(MIMEText(message, 'html'))

    try:
        # Stops the logger and returns print functionality to normal. Also, the log file is closed
        logger.stop()

        # Opens the file to attach
        attachment = open(LOGFILE_DIR + "/" + LOGFILE, "rb")

        # Creates an instance of MIMEBase
        part = MIMEBase('application', 'octet-stream')

        # Steps to convert the file into a Base64
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % LOGFILE)

        # Closes the open file
        attachment.close()

        # Attaches the file
        email_instance.attach(part)

    except IOError as attachedError:                          # Error to open the file
        attachError = "     Could not open the log file so it is not attached to the email. Exception: "\
                      + str(attachedError) + ".\n"

    try:
        # Sends the message via a SMTP server
        session.sendmail(FROM, mailto, email_instance.as_string())

        print(Fore.GREEN + " ✓" + Fore.RESET)

        if not (attachError is None):
            print(Fore.YELLOW + attachError + Fore.RESET)

    except Exception as sendError:
        print(Fore.RED + " ✖ Error to send the email. Exception: " + str(sendError) + ".\n" + Fore.RESET)
        sys.exit(1)


def print_error_notification_or_send_email(mailto, step):
    """
    Prints a message by console or sends an email when an error occurs during the execution of the measurement
    procedure.

    :param mailto: Email address where to send the error notification if it occurs.
    :param step: Step where the error has occurred.
    """

    print(Fore.RED + "     Aborting the execution...\r" + Fore.RESET)

    # Sends an email depending on whether the user entered an email address when the code was run
    if mailto is None:
        print(Fore.CYAN + "     Information!" + Fore.RESET + " Consider enabling the error notification by email to"
                          " receive an informative email instantly. To do this, use the -e/--email option or type"
                          " -h/--help option to get more information.")
    else:
        __send_email_measurement_error(mailto, step)


def disconnect():
    """
    Disconnects the mail session.
    """

    global session

    if not (session is None):
        print("      Disconnecting the mail session"),

        time.sleep(0.25)

        try:
            session.quit()                                    # Ends the mail session
            session = None
            print(Fore.GREEN + " ✓" + Fore.RESET)
        except Exception:
            print(Fore.RED + " ✕" + Fore.RESET)
            raise

        time.sleep(0.25)
