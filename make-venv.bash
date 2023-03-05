#!/bin/bash

# Exit if any command returns with non-zero value
set -e

TARGET_PATH=${1}
REL_PATH_BIN=bin
REL_PATH_ACTIVATE=${REL_PATH_BIN}/activate

# Install local Python installation
# Fails to install without the --without-pip flag.
# Bootstrap install pip inside virtual environment.
echo "Installing Python 3 locally, without pip"
/usr/bin/env python3 -m venv ${TARGET_PATH} --without-pip

echo "Downloading pip installer"
cd ${TARGET_PATH}
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Activate the local Python installation
source ${REL_PATH_ACTIVATE}
echo "Installing pip"
python get-pip.py

echo "Installing mpmath"
pip install mpmath==1.1

echo "Installing Sympy"
pip install sympy==1.10.1

echo "Installing pylint"
pip install pylint

echo $'\n\nActivate virtual environment with:'
echo "source ${TARGET_PATH}/${REL_PATH_ACTIVATE}"
echo "Deactivate with:"
echo "source ${HOME}/.bashrc"

