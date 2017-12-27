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
#        PROJECT:     Hyot                                                                                              #
#           FILE:     utils.sh                                                                                          #
#                                                                                                                       #
#          USAGE:     ---                                                                                               #
#                                                                                                                       #
#    DESCRIPTION:     This script provides several utilities                                                            #
#                                                                                                                       #
#        OPTIONS:     ---                                                                                               #
#   REQUIREMENTS:     ---                                                                                               #
#          NOTES:     It must be loaded in the main script                                                              #
#         AUTHOR:     Jesús Iglesias García, jesus.iglesiasg@estudiante.uam.es                                          #
#   ORGANIZATION:     ---                                                                                               #
#        VERSION:     0.1                                                                                               #
#        CREATED:     12/18/17                                                                                          #
#       REVISION:     ---                                                                                               #
#=======================================================================================================================#

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
    printf "\\n${bold}${blue}====================     %s     ====================${reset}\\n" "$@" 
}

# Bold header
e_header_bold () {
     printf "\\n${bold}${black}%s${reset}\\n\\n" "$@"
}

# Bold message
e_message_bold () {
     printf "${bold}${black}%s${reset}\\n\\n" "$@"
}

# Information message
e_info () { 
    printf "${cyan}➜ %s${reset}\\n" "$@" 
}

# Success message
e_success () { 
    printf "${green}✔ %s${reset}\\n" "$@"
}

# Error message
e_error () { 
    printf "${red}✖ %s${reset}\\n" "$@"
}

# Warning message
e_warning () { 
    printf "${yellow}! %s${reset}\\n" "$@"
}

# Header in the 'Help' section
help_header () { 
    printf "\\n${bold}${blue}====================  %s  ====================${reset}\\n" "$@" 
}

# Bold and yellow message in the 'Help' section
help_bold () { 
    printf "${bold}${yellow}%s${reset}" "$@"
}

# Confirmation message
confirmation_message () {
     printf "${bold}%s${reset}" "$@"
}
