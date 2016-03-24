#!/bin/bash

# Ensure there's no old version of soapytest from previous attempts
touch soapytest
rm -rf soapytest

# Clone latest soapytest repo
git clone https://github.com/soapy/soapytest.git

# run tests and transfere files
/usr/bin/env python soaptest/scripts/makeWeb.py
