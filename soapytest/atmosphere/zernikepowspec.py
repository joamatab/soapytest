import numpy
import unittest

from soapy import atmosphere
from soapy import aoSimLib

from astropy.io import fits

import os
FILEPATH = os.path.dirname(os.path.abspath(__file__))


NZERNS = 50
NSCRNS = 100
SCRNSIZE = 512
SUBSCRNSIZE = 256
R0 = 1.

def getZernCoeffs(
        nZerns, nScrns, scrnSize, subScrnSize, r0, subHarmonics=False):

    Zs = aoSimLib.zernikeArray(nZerns+1, subScrnSize)
    piston = Zs[0]
    Zs = Zs[1:]
    Zs.shape = nZerns, subScrnSize*subScrnSize

    subsPerScrn = scrnSize/subScrnSize
    zCoeffs = numpy.zeros((nZerns, nScrns*(subsPerScrn**2)))

    i = 0
    for n in range(nScrns):
        # Make one big screen
        if subHarmonics:
            scrn = atmosphere.ft_sh_phase_screen(
                    r0, scrnSize, 1./subScrnSize, 100., 0.01)
        else:
            scrn = atmosphere.ft_phase_screen(
                    r0, scrnSize, 1./subScrnSize, 100., 0.01)

        # Pick out as many sub-scrns as possible to actually test
        for x in range(subsPerScrn):
            for y in range(subsPerScrn):
                subScrn = scrn[
                        x*subScrnSize: (x+1)*subScrnSize,
                        y*subScrnSize: (y+1)*subScrnSize]
                subScrn = subScrn.reshape(subScrnSize*subScrnSize)

                # Turn into radians. r0 defined at 500nm, scrns in nm
                # subScrn /= (500/(2*numpy.pi))

                # Dot with zernikes to get powerspec
                zCoeffs[:, i] = (Zs*subScrn).sum(1)/piston.sum()
                i+=1

    return zCoeffs


def loadNoll(nZerns):
    """
    Loads the noll reference values for Zernike variance in Kolmogorov turbulence.
    """
    nollPath = os.path.join(FILEPATH, "../../resources/noll.fits")
    noll = fits.getdata(nollPath)

    return noll.diagonal()[:nZerns]


def plotZernSpec(zVar, noll, filename=None, show=False):

    plt.figure()
    plt.semilogy(zVar, label="Phase Screens")
    plt.semilogy(noll, label="Noll reference")

    plt.xlabel("Zernike mode index")
    plt.ylabel("Power ($rad^2$)")

    plt.legend(loc=0)

    if filename!=None:
        plt.savefig(filename)
    if show:
        plt.show()

if __name__=="__main__":

    # Number of scrns to average over
    nScrns = 200
    r0 = 1. # R0 value to use in test
    nZerns = 50
    subScrnSize = 256
    scrnSize = 512


    zVar, noll = testZernSpec()
    plotZernSpec(zVar, noll, "zernikeVariance.pdf")
