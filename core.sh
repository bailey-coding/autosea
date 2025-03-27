#!/usr/bin/env bash

# Source module files and env file. 
source ./data/.env || { echo "Error sourcing .env file, please make sure you've copied .env.example to ./data/.env and filled out all API keys and/or tokens"; exit 1; }
source ./modules-bash/virustotal.sh || { echo "Error sourcing .virustotal tools, exiting."; exit 1; }
source ./modules-bash/basics.sh || { echo "Error sourcing .core tools, exiting."; exit 1; }

# install base reqs
install_requirements=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --install-requirements)
            install_requirements=true
            shift
            ;;        
        --user-agent)
            python3 python-modules/user_agent_config.py
            shift
            ;;
        *)
            break
            ;;
    esac
done

if [ "$install_requirements" = true ]; then
    if command -v dnf &>/dev/null; then
        echo "Using DNF package manager"
        sudo dnf install -y python3 python3-pip
        python3 -m pip install -r ./data/python-requrements.txt -qqq
    elif command -v yum &>/dev/null; then
        echo "Using Yum package manager"
        sudo yum install -y python3 python3-pip
        python3 -m pip install -r ./data/python-requrements.txt -qqq
    elif command -v apt &>/dev/null; then
        # Use apt on Debian based systems (Ubuntu, Debian)
        echo "Using APT package manager"
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
        python3 -m pip install -r ./data/python-requrements.txt -qqq
    else
        echo "Unsupported package manager or not found"
        exit 1
    fi
    exit 0
fi


if [ ! -f "${BASH_REQUIREMENTS_YAML}" ]; then
    echo "Error: YAML file '${BASH_REQUIREMENTS_YAML}' not found."
    exit 1
fi

# check to make sure required software is installed and ready to go.
__CheckInstalledSoftware__ "${BASH_REQUIREMENTS_YAML}"
# Collect missing requirements
missing_requirements=()
for requirement in "${requirements[@]}"; do
    if ! command -v "$requirement" > /dev/null 2>&1; then
        missing_requirements+=("$requirement")
    fi
done

# Print missing requirements
if [ ${#missing_requirements[@]} -gt 0 ]; then
    echo "Error: The following software is not installed on the system:"
    printf '  - %s\n' "${missing_requirements[@]}"
    exit 1
fi

# Input check and URL formatter reference.
if [ -z "$1" ]; then
    echo "Please supply one or multiple URLs, like so."
    echo "$0 https://example.com"
    echo "OR"
    echo "$0 https://example.com https://example.net https://example.top"
    exit 3
fi

# Meat and Potatoes, referencing all the needed functions via Python scripts.
for i; do
    # Deobfuscate the URL
    deobscufator_url=$(python3 ./modules-python/deobscufator.py "${i}")
    exit_code=$?

    if [ $exit_code -ne 0 ]; then
        echo "Error deobfuscating URL: ${i}, please use Abuse Case Cleaner."
        exit $exit_code
    fi

    echo "=================="
    echo "Input Domain: ${i}"
    echo "De-Obscufated Domain: ${deobscufator_url}"
    
    # run the deobscufated URL through a parser to verify deobscufated domain is actually a URL, if true continue

    python3 ./modules-python/basics.py url_formatter "${deobscufator_url}"
    python3 ./modules-python/basics.py curl_headers "${deobscufator_url}"
    python3 ./modules-python/basics.py host_lookup "${deobscufator_url}"
    python3 ./modules-python/virustotal.py "${deobscufator_url}" "$VTAPI_KEY"
    echo "=================="
    echo ""
done


