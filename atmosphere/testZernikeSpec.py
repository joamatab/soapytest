import numpy

from soapy import atmosphere

from aotools.circle import zernike

import matplotlib.pylab as plt
from astropy.io import fits

import os
FILEPATH = os.path.dirname(os.path.abspath(__file__))

def getZernCoeffs(nZerns, nScrns, scrnSize, subScrnSize, r0):

    Zs = zernike.zernikeArray(nZerns+1, subScrnSize)[1:]

    Zs.shape = nZerns, subScrnSize*subScrnSize

    subsPerScrn = scrnSize/subScrnSize
    zCoeffs = numpy.zeros((nZerns, nScrns*(subsPerScrn**2)))

    i = 0
    for n in range(nScrns):
        # Make one big screen
        scrn = atmosphere.ft_phase_screen(
                r0, scrnSize, 1./subScrnSize, 100., 0.01)

        # Pick out as many sub-scrns as possible to actually test
        for x in range(subsPerScrn):
            for y in range(subsPerScrn):
                subScrn = scrn[
                        x*subScrnSize: (x+1)*subScrnSize,
                        y*subScrnSize: (y+1)*subScrnSize]
                subScrn = subScrn.reshape(subScrnSize*subScrnSize)

                # Dot with zernikes to get powerspec
                zCoeffs[:, i] = (Zs*subScrn).sum(1)
                i+=1

    return zCoeffs


def loadNoll():

    pass

if __name__=="__main__":

    # Number of scrns to average over
    nScrns = 500
    r0 = 1. # R0 value to use in test
    nZerns = 50
    subScrnSize = 256
    scrnSize = 512

    #zCoeffs = testNollSpectrum(nZerns, nScrns, scrnSize, subScrnSize, r0)
