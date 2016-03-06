#! /usr/bin/env python

import os

SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../")

PLOTS_DIR = os.path.join(SOAPYTEST_DIR, "plots/")

def transfer():
    plotfiles = os.listdir('plots')

    for f in plotfiles:
        os.system('scp {}/{} d70j6c@mira.dur.ac.uk:~/public_html/soapytest/'.format(PLOTS_DIR, f))

if __name__=="__main__":
    transfer()
