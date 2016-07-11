#! /usr/bin/env python

from soapytest import plotting

def makePlots(outputdir=None):
    # Atmospehre Plots
    plotting.plotatmos.plotZernSpec(outputdir)
    plotting.plotatmos.plotPhaseVariance(outputdir)

    # SH WFS plots
    plotting.plotshwfs.plotSHPixelScale(outputdir)
    plotting.plotshwfs.plotSHSlopeVariance(outputdir)
    
    # Gradient wfs plots
    plotting.plotgradwfs.plotGradPixelScale(outputdir)
    plotting.plotgradwfs.plotGradSlopeVariance(outputdir)

    # LOS plots
    plotting.plotlineofsight.plotPhaseVariance(outputdir)
    plotting.plotlineofsight.plotPhaseVariance_vs_scrnSize(outputdir)

if __name__=='__main__':
    makePlots()
