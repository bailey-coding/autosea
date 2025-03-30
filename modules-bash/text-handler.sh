#!/usr/bin/env bash

# Text Color Variables
COLOR_RESET='\033[0m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_RED='\033[0;31m'
COLOR_CYAN='\033[0;36m'
COLOR_MAGENTA='\033[0;35m'
COLOR_BOLD='\033[1m'

# Helper functions for colored text
info() {
    echo -e "${COLOR_CYAN}$*${COLOR_RESET}"
}

success() {
    echo -e "${COLOR_GREEN}$*${COLOR_RESET}"
}

warn() {
    echo -e "${COLOR_YELLOW}$*${COLOR_RESET}"
}

error() {
    echo -e "${COLOR_RED}$*${COLOR_RESET}"
}

highlight() {
    echo -e "${COLOR_MAGENTA}${COLOR_BOLD}$*${COLOR_RESET}"
}
