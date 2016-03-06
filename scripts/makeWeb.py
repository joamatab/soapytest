#! /usr/bin/env python

import os
SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))

import sys
sys.path.append(SCRIPTS_DIR)

import makeplots, transferToWeb


def makeWeb():
    try:
        makeplots.makePlots()
    except:
        pass
        
    transferToWeb.transfer()

if __name__ == '__main__':
    makeWeb()
