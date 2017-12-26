#!/bin/bash
#===========================================================================================================================#
#        PROJECT:           Hyot                                                                                            #
#           FILE:           raspberrypi_setup.sh                                                                            #
#                                                                                                                           #
#          USAGE:           bash raspberrypi_setup.sh {--help|--verbose} || ./raspberrypi_setup.sh {--help|--verbose}       #
#                                                                                                                           #
#    DESCRIPTION:           This script sets up the Raspberry Pi                                                            #
#                                                                                                                           #
#        OPTIONS:           ---                                                                                             #
#   REQUIREMENTS:           Root user, Linux-GNU platform                                                                   #
#          NOTES:           It must be run on a Raspberry Pi preferably with Raspbian as operating system                   #
#         AUTHOR:           Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                        #
#   ORGANIZATION:           ---                                                                                             #
#        VERSION:           0.1                                                                                             #
#        CREATED:           12/18/17                                                                                        #
#       REVISION:           ---                                                                                             #
#===========================================================================================================================#

########################################
#             VARIABLES                #
########################################
SETUPFILE="raspberrypi_setup.sh"                        # Name of this file
CWD="$(pwd)"                                            # Current directory
UTILS="utils.sh"                                        # File of utilities
VERBOSE=false                                           # Verbose mode
PIDOFCOMMAND="pidof"                                    # 'pidof' command
COMMANDLINETOOL="apt-get apt-cache apt"                 # 'apt-get', 'apt' and 'apt-cache' tools
RASPICONFIGCOMMAND="raspi-config"                       # 'raspi-config' command
INTERFACES="i2c camera"                                 # Interfaces to enable
REBOOTCOMMAND="reboot"                                  # 'reboot' command

########################################
#             FUNCTIONS                #
########################################

# Loads the utilities ('utils.sh' file)
load_utils () {

    source $CWD/$UTILS
    rc=$?                       # Captures the return code          
    
    if [ $rc -ne 0 ]; then      # Checks the return code of the 'source' command
        exit 1
    fi
}

# Checks that the script is executed as a root user
check_root () {

    if (( EUID != 0 )); then
        e_error "This script must be run as root." 1>&2
        exit 1
    fi
}

# Checks that the script is executed on a Linux platform
check_platform () {

    if [[ $OSTYPE != linux* ]]; then
        e_error "This script must be run in a Linux-GNU platform. For example: Raspbian." 1>&2
        exit 1
    fi
}

# Checks whether this script is or not already running
check_concurrency () {

    # Checks whether the 'pidof' command is installed
    if ! [ -x "$(command -v $PIDOFCOMMAND)" ]; then
        e_error "Command: '$PIDOFCOMMAND' not found. Please, install this command to check and avoid the concurrency." 1>&2
        exit 1    
    fi

    # Checks if another instance is run
    for pid in $(pidof -o %PPID -x $1); do
        if [ $pid != $$ ]; then
            e_error "Process: $1 is already running with PID $pid." 1>&2
            exit 1
        fi
    done
}

# Shows the help to the user
show_help () {
    
    help_header "HYOT - HELP FOR THE RASPBERRY PI SETUP"
    echo
    help_bold "USAGE: "
    echo "$0 {--help|--verbose}"
    echo
    help_bold "BASIC OPTIONS:"
    echo
    echo
    echo "   -h, --help                 Shows the help"
    echo "   -v, --verbose              Provides very helpful additional details as to what the code is doing"
    echo
}

# Checks the entered parameters and the quantity
check_parameters () {
    
    # Number of parameters must be 0 or 1
    if [[ "$1" -gt "1" ]]; then
        e_error "Invalid parameter number. Please, type the option '-h' or '--help' to show the help." 1>&2
        exit 1
    else
        if [[ "$1" -eq "1" ]]; then
            case "$2" in
                -h | --help)        # Shows the help          
                    show_help
                    exit 0
                    ;;
                -v | --verbose)     # Enables the verbose mode
                    VERBOSE=true
                    ;;    
                *)                  # Unknown option
                    e_error "Unknown option: $2. Please, type the option '-h' or '--help' to show the help." 1>&2
                    exit 1 
                    ;;
            esac
        fi
    fi    
}

# Outputs the message by console if the verbose mode is enabled
output () {

    if $VERBOSE; then
        printf "$1"
    fi
}

# Checks whether several command line tools are installed ('apt-get', 'apt' and 'apt-cache')
commandLineTools_is_installed () {

    # Checks whether the command exists and is executable
    for tool in $COMMANDLINETOOL; do
        if ! [ -x "$(command -v $tool)" ]; then
            e_error "Command line tool: '$tool' is not installed in the system. Please, install this package before continuing." 1>&2
            exit 1
        fi
    done
}

    fi
}
# Checks whether the 'Camera' and 'I2C' interfaces are enabled
check_interfaces () {

    # Checks whether the 'raspi-config' command exists and is executable
    if ! [ -x "$(command -v $RASPICONFIGCOMMAND)" ]; then
        e_error "Command: '$RASPICONFIGCOMMAND' not found. Please, run this script in a Raspberry Pi with Raspbian platform." 1>&2
        exit 1  
    fi

    for interface in $INTERFACES; do
        output "Checking if the '$interface' interface is enabled.\n"
        
        # Interface enabled
        if [ "$(raspi-config nonint get_$interface)" == 0 ]; then
            e_success "Interface: $interface enabled."
        else  
            # Interface disabled
            if [ "$(raspi-config nonint get_$interface)" == 1 ]; then
                output "Interface disabled. Enabling...\n"

                # Command to enable the interface
                raspi-config nonint do_$interface 0

                e_success "Interface: $interface enabled."
            fi
        fi
        output "\n"
    done
}

# Asks to user whether or not to reboot the system
seek_confirmation() {
    printf "${bold}$@${reset}"
    read -p "${bold} (y/n)${reset} " -n 1
    echo
}

# Tests whether the result is a confirmation
is_confirmed() {
    
    if [[ "$REPLY" =~ ^[Yy]$ ]]; then 
        return 0
    fi
    return 1
}

# Trap keyboard interrupt (ctrl + c)
ctrl_c() {

    echo
    e_error "Exception: KeyboardInterrupt. Please, wait until the process finishes." 1>&2
    exit 130
}

########################################
#             MAIN PROGRAM             #
########################################

# Trap the keyboard interrupt signal
trap ctrl_c SIGINT

load_utils                          # Loads the 'utils.sh' file
check_root                          # Checks that the script is executed as a root user
check_platform                      # Checks that the script is executed in a GNU platform
check_concurrency $SETUPFILE        # Checks if this script is or not already running
check_parameters $# $1              # Checks the parameters and the number of them

# Header                               
e_header "     HYOT - RASPBERRY PI SETUP     "
e_header_bold "This script perfoms several actions to install the packages and libraries needed to execute the 'xx.py' file. Type the '-v' or '--verbose' option to show the trace."

output "Starting the configuration...\n\n"

# Checks whether several command line tools are installed ('apt-get', 'apt' and 'apt-cache')
commandLineTools_is_installed

# Checks whether the 'Camera' and 'I2C' interfaces are enabled
check_interfaces

# Print a line break when 'verbose' mode is disabled
if ! $VERBOSE; then
    printf "\n"
fi

# Process finished
e_message_bold "Process has finished succesfully."

# Asks the user whether or not to reboot the system
seek_confirmation "Do you want to reboot the system? It would be an excellent idea for everything to work correctly!"
# Reboot the system
if is_confirmed; then

    # Checks whether the 'reboot' command exists and is executable
    if ! [ -x "$(command -v $REBOOTCOMMAND)" ]; then
        echo
        e_error "Command: '$REBOOTCOMMAND' not found. Please, reboot the system manually." 1>&2
        exit 1 
    else  # Reboot
        e_message_bold "Rebooting the system..."
        sleep 5
        reboot 
    fi
fi

