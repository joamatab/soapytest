#!/bin/bash
source /home/user/apr/.bashrc

# Make a directory to run tests in 
mkdir ~/CfAI/soapytest/testbuild
cd ~/CfAI/soapytest/testbuild

# Ensure there's no old version of soapytest from previous attempts
touch soapytest
rm -rf soapytest

# Clone latest soapytest repo
git clone https://github.com/soapy/soapytest.git
cd soapytest
# run tests and transfere files
/usr/bin/env python scripts/makeWeb.py

# Clean up
rm -rf ~/CfAI/soapytest/testbuild
