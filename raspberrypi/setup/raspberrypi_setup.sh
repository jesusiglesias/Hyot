#!/bin/bash
#=======================================================================================================================#
#                                                                                                                       #
#                                    __    __   ___      ___   ________    __________                                   #
#                                   |  |  |  |  \  \    /  /  |   __   |  |___    ___|                                  #
#                                   |  |__|  |   \  \__/  /   |  |  |  |      |  |                                      #
#                                   |   __   |    \_|  |_/    |  |  |  |      |  |                                      #
#                                   |  |  |  |      |  |      |  |__|  |      |  |                                      #
#                                   |__|  |__|      |__|      |________|      |__|                                      #
#                                                                                                                       #
#                                                                                                                       #
#        PROJECT:   Hyot                                                                                                #
#           FILE:   raspberrypi_setup.sh                                                                                #
#                                                                                                                       #
#          USAGE:   sudo bash raspberrypi_setup.sh {--help|--verbose} || sudo ./raspberrypi_setup.sh {--help|--verbose} #
#                                                                                                                       #
#    DESCRIPTION:   This script sets up the Raspberry Pi                                                                #
#                                                                                                                       #
#        OPTIONS:   ---                                                                                                 #
#   REQUIREMENTS:   Root user, Linux-GNU platform                                                                       #
#          NOTES:   It must be run with root user on a Raspberry Pi preferably with Raspbian as operating system        #
#         AUTHOR:   Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                            #
#   ORGANIZATION:   ---                                                                                                 #
#        VERSION:   0.1                                                                                                 #
#        CREATED:   12/18/17                                                                                            #
#       REVISION:   01/02/18                                                                                            #
#=======================================================================================================================#

########################################
#             VARIABLES                #
########################################
SETUPFILE="raspberrypi_setup.sh"                        # Name of this file
CWD="$(pwd)"                                            # Current directory
UTILS="utils.sh"                                        # File of utilities
VERBOSE=false                                           # Verbose mode
PIDOFCOMMAND="pidof"                                    # 'pidof' command
WGETCOMMAND="wget"                                      # 'wget' command
COMMANDLINETOOL="apt-get apt-cache dpkg"                # 'apt-get', 'apt-cache' and 'dpkg' tools
PACKAGESTOINSTALL="python2.7 build-essential python-dev python-smbus python-pip i2c-tools"        # Packages to install
LIBRARYTOINSTALL="psutil pyfiglet colorama RPi.GPIO Adafruit_Python_DHT RPLCD ibmiotf picamera"   # Libraries to install
RASPICONFIGCOMMAND="raspi-config"                       # 'raspi-config' command
INTERFACES="i2c camera"                                 # Interfaces to enable
REBOOTCOMMAND="reboot"                                  # 'reboot' command

########################################
#             FUNCTIONS                #
########################################

# Loads the utilities ('utils.sh' file)
load_utils () {

    # shellcheck source=./utils.sh
    source "$CWD"/"$UTILS"
    rc=$?                       # Captures the return code          
    
    if [ ${rc} -ne 0 ]; then    # Checks the return code of the 'source' command
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

# Checks that the script is executed on GNU/Linux platform
check_platform () {

    if [[ $OSTYPE != linux* ]]; then
        e_error "This script must be run on GNU/Linux platform. For example: Raspbian." 1>&2
        exit 1
    fi
}

# Checks that the script is executed on a Raspberry pi
check_raspberrypi () {

    # Checks the '/proc/cpuinfo' file to obtain the 'Hardware' field value. Possible values:
    #   - Raspberry Pi 1 (model A, B, B+) and Zero is 2708
    #   - Raspberry Pi 2 (model B) is 2709
    #   - Raspberry Pi 3 (model B) on 4.9.x kernel is 2835
    #   - Anything else is not a Raspberry Pi

    # '/proc/cpuinfo' file does not exist
    if ! [ -e "/proc/cpuinfo" ]; then
        e_error "No such file or directory: '/proc/cpuinfo'. This script must be run on a Raspberry Pi." 1>&2
        exit 1
    else
        hardware="$(cat /proc/cpuinfo | grep 'Hardware' | awk '{print $3}')"

        if [[ ${hardware} != "BCM2708" && ${hardware} != "BCM2709" && ${hardware} != "BCM2835" ]]; then
            e_error "This script must be run on a Raspberry Pi." 1>&2
            exit 1
        fi
    fi
}

# Checks if the Raspberry Pi is connected to the network
check_network () {

    # Checks if the 'wget' command is installed
    if ! [ -x "$(command -v ${WGETCOMMAND})" ]; then
        e_error "Command: 'WGETCOMMAND' not found. Please, install this command to check if the network connection is available." 1>&2
        exit 1
    fi

    # Checks if Google can be reached. Some places have a firewall that blocks all traffic except via a web proxy.
    # For this reason, a ping is not performed
    wget -q --tries=5 --timeout=20 --spider http://google.com>/dev/null
    if [[ $? -ne 0 ]]; then
        e_error "Raspberry Pi is not connected to the network. Please, enable the network to continue the setup." 1>&2
        exit 1
    fi
}

# Checks if this script is or not already running
check_concurrency () {

    # Checks if the 'pidof' command is installed
    if ! [ -x "$(command -v ${PIDOFCOMMAND})" ]; then
        e_error "Command: '$PIDOFCOMMAND' not found. Please, install this command to check and avoid the concurrency." 1>&2
        exit 1    
    fi

    # Checks if another instance is run
    for pid in $(pidof -o %PPID -x "$1"); do
        if [ "$pid" != "$$" ]; then
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
    echo "sudo $0 {--help|--verbose}"
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

    if ${VERBOSE}; then
        printf "%b" "$1"
    fi
}

# Print a line break when 'verbose' mode is disabled
lineBreak () {
    
    if ! ${VERBOSE}; then
        printf "\\n"
    fi
}

# Checks if several command line tools are installed ('apt-get', 'apt-cache' and 'dpkg')
commandLineTools_is_installed () {

    # Checks if the command exists and is executable
    for tool in ${COMMANDLINETOOL}; do
        if ! [ -x "$(command -v "$tool")" ]; then
            e_error "Command line tool: '$tool' is not installed in the system. Please, install this package before continuing." 1>&2
            exit 1
        fi
    done
}

# Checks if the packages are installed and updated in the system
# shellcheck disable=SC2143
package_is_installed () {

    # Checks if the package exists
    if [ "$(dpkg -l "$1" | grep '^'"ii"'\s')" ]; then
        output "Package is installed. Checking if this one is updated.\\n"

        # Package is outdated
        if [ "$(apt-get -V --assume-no upgrade | grep '\s'"$1"'\s')" ]; then
            output "Package should be updated. Updating...\\n"

            # Command to update the package
            apt-get --only-upgrade install "$1" -y>/dev/null
            return_value_aptget_update=$?                   # Obtains the result

            # Error to update the package
            if [ ${return_value_aptget_update} -ne 0 ]; then
                e_error "Error to update the $1 package." 1>&2
                exit 1
            fi
        else
            output "Package is already updated to the last version.\\n"
        fi   
        e_info "Package: '$1' is installed and updated in the system."
    else
        output "Package is not installed. Searching the package in the repository...\\n"

        # Package exists in the repository
        if [ "$(apt-cache search "$1" | grep '^'"$1"'\s')" ]; then
            output "Package has been found. Installing...\\n"

            # Command to install the package
            apt-get install "$1" -y>/dev/null
            return_value_aptget_install=$?                  # Obtains the result

            # Error to install the package
            if [ ${return_value_aptget_install} -ne 0 ]; then
                e_error "Error to install the $1 package." 1>&2
                exit 1
            fi

            e_success "Package: '$1' was installed successfully."
        else
            e_error "Package: '$1' not found in the repository. Please, check its name." 1>&2
        fi 
    fi
}

# Checks if the libraries are installed and updated in the system
# shellcheck disable=SC2143
library_is_installed () {

    # Checks if the library is installed
    if [ "$(pip show "$1")" ]; then
        output "Library is installed. Checking if this one is updated.\\n"

        # Library is outdated
        if [ "$(pip search "$1" | grep -A2 '^'"$1"'\s' | grep -B2 'LATEST:')" ]; then 
            output "Library should be updated. Updating...\\n"

            # Command to update the library
            pip install --upgrade "$1">/dev/null
            return_value_pip_update=$?                          # Obtains the result

            # Error to update the library
            if [ ${return_value_pip_update} -ne 0 ]; then
                e_error "Error to update the $1 library." 1>&2
                exit 1
            fi
        else
            output "Library is already updated to the last version.\\n"
        fi   
        e_info "Library: '$1' is installed and updated in the system."
    else
        output "Library is not installed. Searching the library in the repository...\\n"

        # Library exists in the repository
        if [ "$(pip search "$1" | grep '^'"$1"'\s')" ]; then 
            output "Library has been found. Installing...\\n"

            # Command to install the library
            pip install "$1">/dev/null
            return_value_pip_install=$?                         # Obtains the result

            # Error to install the library
            if [ ${return_value_pip_install} -ne 0 ]; then
                e_error "Error to install the $1 library." 1>&2
                exit 1
            fi

            e_success "Library: '$1' was installed successfully."
        else
            e_error "Library: '$1' not found in the repository. Please, check its name." 1>&2
        fi
    fi
}

# Checks if the 'Camera' and 'I2C' interfaces are enabled
check_interfaces () {

    # Checks if the 'raspi-config' command exists and is executable
    if ! [ -x "$(command -v ${RASPICONFIGCOMMAND})" ]; then
        e_error "Command: '$RASPICONFIGCOMMAND' not found. Please, run this script in a Raspberry Pi with Raspbian platform." 1>&2
        exit 1  
    fi

    for interface in ${INTERFACES}; do
        output "Checking if the '$interface' interface is enabled.\\n"
        
        # Interface enabled
        if [ "$(raspi-config nonint get_"$interface")" == 0 ]; then
            e_success "Interface: $interface enabled."
        else  
            # Interface disabled
            if [ "$(raspi-config nonint get_"$interface")" == 1 ]; then
                output "Interface disabled. Enabling...\\n"

                # Command to enable the interface
                raspi-config nonint do_"$interface" 0
                return_value_raspi_config=$?                    # Obtains the result

                # Error to enable the interface
                if [ ${return_value_raspi_config} -ne 0 ]; then
                    e_error "Error to enable the $interface interface." 1>&2
                    exit 1
                fi

                e_success "Interface: $interface enabled."
            fi
        fi
        output "\\n"
    done
}

# Asks to user whether or not to reboot the system
seek_confirmation() {
    confirmation_message "$1"
    # shellcheck disable=SC2162
    read -p "$(confirmation_message " (y/n) ")" -n 1
    echo
}

# Tests if the result is a confirmation
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
check_platform                      # Checks that the script is executed on GNU/Linux platform
check_raspberrypi                   # Checks that the script is executed on a Raspberry pi
check_network                       # Checks if the Raspberry Pi is connected to the network
check_concurrency ${SETUPFILE}      # Checks if this script is or not already running
check_parameters "$#" "$1"          # Checks the parameters and the number of them

# Header                               
e_header "     HYOT - RASPBERRY PI SETUP     "
e_header_bold "This script performs several actions to install the packages and libraries needed to execute the 'raspberrypi_hyot.py' file. Type the '-v' or '--verbose' option to show the trace."

output "Starting the configuration...\\n\\n"

# Checks if several command line tools are installed ('apt-get', 'apt-cache' and 'dpkg')
commandLineTools_is_installed

# Checks if each package is installed and updated. If not, it is installed or updated
for package in ${PACKAGESTOINSTALL}; do
    output "Checking if the '$package' package is installed and updated.\\n"
    package_is_installed "$package"
    output "\\n"
done

# Print a line break when 'verbose' mode is disabled
lineBreak

# Checks if each library is installed and updated. If not, it is installed or updated
for library in ${LIBRARYTOINSTALL}; do
    output "Checking if the '$library' library is installed and updated.\\n"
    library_is_installed "$library"
    output "\\n"
done

# Print a line break when 'verbose' mode is disabled
lineBreak

# Checks if the 'Camera' and 'I2C' interfaces are enabled
check_interfaces

# Print a line break when 'verbose' mode is disabled
lineBreak

# Process finished
e_message_bold "Process has finished successfully."

# Asks the user whether or not to reboot the system
seek_confirmation "Do you want to reboot the system? It would be an excellent idea for everything to work correctly!"
# Reboot the system
if is_confirmed; then

    # Checks if the 'reboot' command exists and is executable
    if ! [ -x "$(command -v ${REBOOTCOMMAND})" ]; then
        echo
        e_error "Command: '$REBOOTCOMMAND' not found. Please, reboot the system manually." 1>&2
        exit 1 
    else  # Reboot
        e_header_bold "Rebooting the system..."
        sleep 5
        reboot 
    fi
fi
