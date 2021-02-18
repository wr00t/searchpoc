#!/bin/sh

version=1.0.6
url="https://raw.githubusercontent.com/5amu/searchpoc/$version/searchpoc.py"

err() { echo >&2 "$(tput bold; tput setaf 1)[-] ERROR: ${*}$(tput sgr0)"; exit 1; }
msg() { echo "$(tput bold; tput setaf 2)[+] ${*}$(tput sgr0)"; }

# Check dependencies and privileges
msg "Checking dependencies and privileges"
command -v python3 >/dev/null || err "Install Python3"
[ "$(id -u)" -ne 0 ] && err "You must be root"

# Making a temporary directory
msg "Preparing the environment"
_tmp=$( mktemp -d /tmp/searchpoc.XXXXXXX )

# Intercept SIGINT and deleting the files if aborting
trap "rm -rf $_tmp" SIGINT

# Download the script
msg "Downloading the script"
wget "$url" -O "${_tmp}/searchpoc.py" || err "Download failed"

msg "Installing..."
install -Dm755 "${_tmp}/searchpoc.py" /usr/bin/searchpoc || err "Installation failed"

msg "Done!"
