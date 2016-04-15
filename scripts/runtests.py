#!/usr/bin/env python
import os
import sys
import subprocess
import shutil


CONDA_PACKAGES = ['numpy', 'numba', 'scipy', 'pip']
PIP_PACKAGES = []# ['pyfftw']
SOAPY_VER = "v0.11.0"

os.environ["PYTHONPATH"] = ""

SOAPYTEST_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
SOAPYTEST_BUILD_PATH = os.path.join(SOAPYTEST_PATH, 'soapytest_build')
if sys.platform=="darwin":
    CONDA_LINK = "https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh"
elif sys.platform == "linux2":
    CONDA_LINK = "https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh"


# If its already there - remove the build dir
if os.path.exists(SOAPYTEST_BUILD_PATH):
    shutil.rmtree(SOAPYTEST_BUILD_PATH)
# And make a new one to start from scratch
os.makedirs(SOAPYTEST_BUILD_PATH)

subprocess.call(["wget", CONDA_LINK, "-O", "miniconda.sh"])
subprocess.call(["chmod", "+x", "miniconda.sh"])
subprocess.call(["./miniconda.sh", "-b", "-p", "{}/miniconda".format(SOAPYTEST_BUILD_PATH)])
os.environ["PATH"] = "{0}/miniconda/bin:{1}".format(SOAPYTEST_BUILD_PATH, os.environ["PATH"])
print(os.environ["PATH"])
subprocess.call(['conda', "update", "--yes", "conda"])
subprocess.call(['conda', 'install', '--yes']+CONDA_PACKAGES)
subprocess.call(['pip', 'install']+PIP_PACKAGES)

# Get soapy
git_install('soapy', 'https://github.com/soapy/soapy.git')

# install aotools
git_install('aotools', 'https://github.com/soapy/aotools.git')

# Install soapytest
git_install('soapytest', 'https://github.com/soapy/soapytest.git')

from soapytest import makeplots, transfertoweb

# make plots
os.makedirs('plots')
os.environ["PYTHONPATH"] = "{}:{}".format(os.path.join(SOAPYTEST_BUILD_PATH, 'soapytest/scripts'), os.environ["PYTHONPATH"])

# Atmospehre Plots
makeplots.makePlots(os.join(SOAPYTEST_BUILD_PATH, "plots"))

transfertoweb.transfer()




# # Ensure there's no old version of soapytest from previous attempts
# touch soapytest
# rm -rf soapytest
#
# # Clone latest soapytest repo
# git clone https://github.com/soapy/soapytest.git
# cd soapytest
# # Make a plave to put plots
# mkdir plots
# # run tests and transfere files
# python scripts/makeWeb.py
#
# # Clean up
# rm -rf ~/CfAI/soapytest/testbuild
def git_install(name, url):
    subprocess.call(["git", "clone", url])
    subprocess.call(['cd', name])
    subprocess.call(['python', 'setup.py', 'install'])
    subprocess.call(['cd', '..'])
