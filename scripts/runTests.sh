#!/bin/bash
export PATH=/opt/anaconda2/bin:$PATH

# Make a directory to run tests in 
mkdir ~/CfAI/soapytest/testbuild
cd ~/CfAI/soapytest/testbuild

# Ensure there's no old version of soapytest from previous attempts
touch soapytest
rm -rf soapytest

# Clone latest soapytest repo
git clone https://github.com/soapy/soapytest.git
cd soapytest
# Make a plave to put plots
mkdir plots
# run tests and transfere files
python scripts/makeWeb.py

# Clean up
rm -rf ~/CfAI/soapytest/testbuild
