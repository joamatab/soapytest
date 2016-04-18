#!/usr/bin/env python
import os
import sys
import subprocess
import shutil


CONDA_PACKAGES = ['numpy', 'scipy', 'pip', 'astropy']
PIP_PACKAGES = ['pyfftw', 'plotly']
SOAPY_VER = "master"

def git_install(name, url,  tag=None):
    subprocess.call(["git", "clone", url, name])
    os.chdir(name)
    if tag is not None:
        subprocess.call(['git', 'checkout', tag])
    subprocess.call(['python', 'setup.py', 'install'])
    os.chdir(name)

os.environ["PYTHONPATH"] = ""

SOAPYTEST_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
SOAPYTEST_BUILD_PATH = os.path.join(SOAPYTEST_PATH, 'soapytest_build')
if sys.platform=="darwin":
    CONDA_LINK = "https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh"
elif sys.platform == "linux2":
    CONDA_LINK = "https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh"

if __name__=="__main__":


    # If its already there - remove the build dir
    if os.path.exists(SOAPYTEST_BUILD_PATH):
        print("Removing existing build dir...")
        shutil.rmtree(SOAPYTEST_BUILD_PATH)
    # And make a new one to start from scratch
    os.makedirs(SOAPYTEST_BUILD_PATH)
    
    print("Install conda for: {}".format(sys.platform))
    MCONDA_PATH = os.path.join(SOAPYTEST_BUILD_PATH, "miniconda.sh")
    subprocess.call(["wget", CONDA_LINK, "-O", MCONDA_PATH])
    subprocess.call(["chmod", "+x", MCONDA_PATH])
    subprocess.call([MCONDA_PATH, "-b", "-p", "{}/miniconda".format(SOAPYTEST_BUILD_PATH)])
    os.environ["PATH"] = "{0}/miniconda/bin:{1}".format(SOAPYTEST_BUILD_PATH, os.environ["PATH"])
    print("PATH:{}".format(os.environ["PATH"]))
    subprocess.call(['conda', "update", "--yes", "conda"])
    subprocess.call(['conda', 'install', '--yes']+CONDA_PACKAGES)
    subprocess.call(['pip', 'install']+PIP_PACKAGES)

    # Get soapy
    git_install(os.path.join(SOAPYTEST_BUILD_PATH,'soapy'), 'https://github.com/soapy/soapy.git', tag=SOAPY_VER)

    # install aotools
    git_install(os.path.join(SOAPYTEST_BUILD_PATH,'aotools'), 'https://github.com/soapy/aotools.git')

    # Install soapytest
    git_install(os.path.join(SOAPYTEST_BUILD_PATH,'soapytest'), 'https://github.com/soapy/soapytest.git')

    # Run script with conda python to make plots
    scriptpath = os.path.join(SOAPYTEST_BUILD_PATH, 'soapytest/scripts/run.py')
    subprocess.call(['python', scriptpath, SOAPYTEST_BUILD_PATH])

    # clean up
    shutil.rmtree(SOAPYTEST_BUILD_PATH)
