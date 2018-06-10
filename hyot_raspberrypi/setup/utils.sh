#!/bin/bash
# =====================================================================================================================#
#                                                                                                                      #
#                                              _    ___     ______ _______                                             #
#                                             | |  | \ \   / / __ \__   __|                                            #
#                                             | |__| |\ \_/ / |  | | | |                                               #
#                                             |  __  | \   /| |  | | | |                                               #
#                                             | |  | |  | | | |__| | | |                                               #
#                                             |_|  |_|  |_|  \____/  |_|                                               #
#                                                                                                                      #
#                ____                 _                            ____  _    ____       _                             #
#               |  _ \ __ _ ___ _ __ | |__   ___ _ __ _ __ _   _  |  _ \(_)  / ___|  ___| |_ _   _ _ __                #
#               | |_) / _` / __| '_ \| '_ \ / _ \ '__| '__| | | | | |_) | |  \___ \ / _ \ __| | | | '_ \               #
#               |  _ < (_| \__ \ |_) | |_) |  __/ |  | |  | |_| | |  __/| |   ___) |  __/ |_| |_| | |_) |              #
#               |_| \_\__,_|___/ .__/|_.__/ \___|_|  |_|   \__, | |_|   |_|  |____/ \___|\__|\__,_| .__/               #
#                              |_|                         |___/                                  |_|                  #
#                                                                                                                      #
#                                                                                                                      #
#        PROJECT:     Hyot                                                                                             #
#           FILE:     utils.sh                                                                                         #
#                                                                                                                      #
#          USAGE:     sudo bash raspberrypi_setup.sh || sudo ./raspberrypi_setup.sh                                    #
#                                                                                                                      #
#    DESCRIPTION:     This script provides several utilities for the main configuration script                         #
#                                                                                                                      #
#        OPTIONS:     ---                                                                                              #
#   REQUIREMENTS:     ---                                                                                              #
#          NOTES:     It must be loaded in the main configuration script: raspberrypi_setup.sh                         #
#         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  #
#   ORGANIZATION:     ---                                                                                              #
#        VERSION:     1.0.0                                                                                            #
#        CREATED:     12/18/17                                                                                         #
#       REVISION:     01/03/18                                                                                         #
#                                                                                                                      #
# =====================================================================================================================#

########################################
#     COLOR AND MODE CAPABILITIES      #
########################################

# Modes
bold=$(tput bold)                       # Set bold mode
reset=$(tput sgr0)                      # Turn off all attributes

# Colors
black=$(tput setaf 0)
red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
blue=$(tput setaf 4)
cyan=$(tput setaf 6)

########################################
#              LOGGING                 #
########################################

# Header
e_header () {
    printf "\\n${bold}${blue}%s${reset}\\n" "$@"
}

# Bold title
e_title_bold () {
     printf "   ${bold}${black}%s${reset}\\n" "$@"
}

# Bold message
e_message_bold () {
     printf "   ${bold}${black}%s${reset}\\n\\n" "$@"
}

# Information message
e_info () {
    printf "   ${cyan}➜ %s${reset}\\n" "$@"
}

# Success message
e_success () {
    printf "   ${green}✔ %s${reset}\\n" "$@"
}

# Error message
e_error () {
    printf "${red}✖ %s${reset}\\n" "$@"
}

# Error message with initial spaces
e_error_initialspaces () {
    printf "   ${red}✖ %s${reset}\\n" "$@"
}

# Error message with initial spaces and two break lines
e_error_spaces () {
    printf "   ${red}✖ %s${reset}\\n\\n" "$@"
}

# Error traceback
e_error_traceback () {
    printf "   ${red}Traceback: %s${reset}\\n\\n" "$@"
}

# Warning message
e_warning () {
    printf "${yellow}! %s${reset}\\n" "$@"
}

# Header in the 'Help' section
help_header () {
    printf "${bold}${cyan}====================  %s  ====================${reset}\\n" "$@"
}

# Bold and yellow message in the 'Help' section
help_bold () {
    printf "${bold}${yellow}%s${reset}" "$@"
}

# Confirmation message
confirmation_message () {
     printf "${bold}%s${reset}" "$@"
}
