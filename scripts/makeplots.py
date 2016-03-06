#! /usr/bin/env python

from soapytest import plotting

def makePlots():
    # Atmospehre Plots
    plotting.plotatmos.plotZernSpec()

    # SH WFS plots
    plotting.plotshwfs.plotSHPixelScale()


if __name__=='__main__':
    makePlots()
