#! /usr/bin/env python

import os
SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
SOAPYTEST_DIR = os.path.join(SCRIPTS_DIR, '..')
SOAPY_DIR = os.path.join(SOAPYTEST_DIR, '../soapy')
import sys
sys.path.append(SCRIPTS_DIR)
sys.path.append(SOAPYTEST_DIR)

import makeplots, transferToWeb


def makeWeb():
    try:
        makeplots.makePlots()
    except KeyboardInterrupt:
        pass
    transferToWeb.transfer()

if __name__ == '__main__':
    makeWeb()
