#!/usr/bin/env python
import os
import sys
import subprocess
import shutil


CONDA_PACKAGES = ['numpy', 'numba', 'scipy', 'pip']
PIP_PACKAGES = []# ['pyfftw']
SOAPY_VER = "v0.11.0"

def git_install(name, url, tag=None):
    subprocess.call(["git", "clone", url])
    subprocess.call(['cd', name])
    if tag is not None:
        subprocess.call(['git', 'checkout', tag])
    subprocess.call(['python', 'setup.py', 'install'])
    subprocess.call(['cd', '..'])


os.environ["PYTHONPATH"] = ""

SOAPYTEST_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
SOAPYTEST_BUILD_PATH = os.path.join(SOAPYTEST_PATH, 'soapytest_build')
if sys.platform=="darwin":
    CONDA_LINK = "https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh"
elif sys.platform == "linux2":
    CONDA_LINK = "https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh"

if __name__=="__main__":

    # If its already there - remove the build dir
    if os.path.exists(SOAPYTEST_BUILD_PATH):
        print("Removing existing build dir...")
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
    git_install('soapy', 'https://github.com/soapy/soapy.git', tag=SOAPY_VER)

    # install aotools
    git_install('aotools', 'https://github.com/soapy/aotools.git')

    # Install soapytest
    git_install('soapytest', 'https://github.com/soapy/soapytest.git')

    from soapytest import makeplots, transfertoweb

    # make plots
    PLOT_DIR = os.path.join(SOAPYTEST_BUILD_PATH, 'plots/')
    os.makedirs(PLOT_DIR)
    os.environ["PYTHONPATH"] = "{}:{}".format(os.path.join(SOAPYTEST_BUILD_PATH, 'soapytest/scripts'), os.environ["PYTHONPATH"])

    # makeplots.makePlots(PLOT_DIR)
    #
    # transfertoweb.transfer(PLOT_DIR)

    # clean up
    shutil.rmtree(SOAPYTEST_BUILD_PATH)
    os.remove('miniconda.sh')
