#! /usr/bin/env python

from soapytest import plotting

def makePlots(outputdir=None):
    # Atmospehre Plots
    plotting.plotatmos.plotZernSpec(outputdir)

    # SH WFS plots
    plotting.plotshwfs.plotSHPixelScale(outputdir)
    plotting.plotshwfs.plotSHSlopeVariance(outputdir)
    
    # Gradient wfs plots
    plotting.plotgradwfs.plotGradPixelScale(outputdir)
    plotting.plotgradwfs.plotGradSlopeVariance(outputdir)

if __name__=='__main__':
    makePlots()
