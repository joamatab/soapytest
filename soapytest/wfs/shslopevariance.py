import numpy

from soapy import atmosphere, wfs, confParse
from aotools import circle
from aotools import wfs as wfslib


import os
SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")
SOAPY_CONF = os.path.join(SOAPYTEST_DIR, "conf/wfs/shpixelvariance.yaml")

RAD2ASEC = 206264.849159
ASEC2RAD = 1./RAD2ASEC

# How many phase screens to run the tests on
N_SCRNS = 8
N_R0s = 10
R0s = numpy.linspace(0.05, 0.2, N_R0s)

class SHSlopeVariance(object):
    def __init__(self, configfile=SOAPY_CONF):

        self.configfile = SOAPY_CONF
        self.loadConfig()


    def loadConfig(self):
        """
        Load the Soapy config file
        """
        self.config = confParse.loadSoapyConfig(self.configfile)

        self.nIters = self.config.sim.nIters

        self.mask = circle.circle(
                self.config.sim.pupilSize/2., self.config.sim.simSize)

        self.wfsPixelScale = self.config.wfss[0].subapFOV/self.config.wfss[0].pxlsPerSubap

        # Initialise the WFS (can use same one for all tests)
        self.wfs = wfs.ShackHartmann(self.config, mask=self.mask)


    def run_scrns(self):


        slopes = numpy.zeros((N_SCRNS * self.nIters, 2, self.wfs.activeSubaps))

        for iscrn in range(N_SCRNS):
            atmos = atmosphere.atmos(self.config)
            print('Made screen - starting run')
            for i in range(self.nIters):
                fullSlopes = self.wfs.frame(atmos.moveScrns())
                slopes[iscrn*self.nIters + i, 0] = fullSlopes[:self.wfs.activeSubaps]
                slopes[iscrn*self.nIters + i, 1] = fullSlopes[self.wfs.activeSubaps:]
        return slopes

    def run_allR0s(self):

        slopes = numpy.zeros((N_R0s, N_SCRNS * self.nIters, 2, self.wfs.activeSubaps))

        for ir0, r0 in enumerate(R0s):
            print(f"Test R0: {r0}")
            self.config.atmos.r0 = r0
            slopes[ir0] = self.run_scrns()

        return slopes


    def getR0fromSlopes(self, slopes):
        # Convert slopes to radians
        slopes_rad = slopes * self.wfsPixelScale * ASEC2RAD

        measuredR0s = numpy.zeros((N_R0s))
        subapDiam = self.config.tel.telDiam/self.config.wfss[0].nxSubaps

        for i in range(N_R0s):
            measuredR0s[i] = wfslib.r0fromSlopes(
                    slopes_rad[i], self.config.wfss[0].wavelength, subapDiam)

        return measuredR0s

    def runTest(self):

        slopes_asec = self.run_allR0s()
        measuredR0s = self.getR0fromSlopes(slopes_asec)

        return R0s, measuredR0s

def runTest():
    SHVR = SHSlopeVariance()
    return SHVR.runTest()

if __name__ == "__main__":

    R0s, measuredR0s = runTest()
