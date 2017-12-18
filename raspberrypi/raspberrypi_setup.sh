#!/bin/bash
#==========================================================================================================#
#        PROJECT:           Hyot                                                                           #
#           FILE:           raspberrypi_setup.sh                                                           #
#                                                                                                          #
#          USAGE:           bash raspberrypi_setup.sh [options] || ./raspberrypi_setup.sh [options]        #
#                                                                                                          #
#    DESCRIPTION:           This script sets up the Raspberry Pi                                           #
#                                                                                                          #
#        OPTIONS:           ---                                                                            #
#   REQUIREMENTS:           Root user, Linux-GNU platform                                                  #
#          NOTES:           It must be run on a Raspberry Pi preferably with Raspbian as operating system  #
#         AUTHOR:           Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                       #
#   ORGANIZATION:           ---                                                                            #
#        VERSION:           0.1                                                                            #
#        CREATED:           12/18/17                                                                       #
#       REVISION:           ---                                                                            #
#==========================================================================================================#

########################################
#             VARIABLES                #
########################################
SETUPFILE="raspberrypi_setup.sh"                # Name of this file
CWD="$(pwd)"                                    # Current directory
UTILS="utils.sh"                                # File of utilities

########################################
#             FUNCTIONS                #
########################################

# Loads the utilities ('utils.sh' file)
load_utils () {

    source $CWD/$UTILS
    rc=$?                                       # Captures the return code          
    
    if [ $rc -ne 0 ]; then                      # Checks the return code of the source command
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

# Checks that the script is executed in a Linux platform
check_platform () {

    if [[ $OSTYPE != linux* ]]; then
        e_error "This script must be run in a Linux-GNU platform. For example: Raspbian." 1>&2
        exit 1
    fi
}

# Checks if this script is or not already running
check_concurrency () {

    for pid in $(pidof -o %PPID -x $1); do
        if [ $pid != $$ ]; then
            e_error "Process: $1 already running with PID $pid." 1>&2
            exit 1
        fi
    done
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
