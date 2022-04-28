import numpy

from soapy import confParse, wfs, aoSimLib

import os
SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")
SOAPY_CONF = os.path.join(SOAPYTEST_DIR, "conf/wfs/gradpixelscale.yaml")

MAXTILT = 5.


class GradPixelScale(object):
    def __init__(self, configfile=SOAPY_CONF):

        self.configfile = configfile
        self.loadConfig()

        self.makeTilt()

        self.maxtilt = None

        self.nTilts = 11
        self.wfs = wfs.Gradient(self.config)

    def loadConfig(self):
        """
        Load the Soapy config file
        """
        self.config = confParse.YAML_Configurator(self.configfile)
        self.config.loadSimParams()

        self.mask = aoSimLib.circle(
                self.config.sim.pupilSize/2., self.config.sim.simSize)

    def makeTilt(self):
        """
        Make a static unit tilt to be used in this test
        """
        coords = numpy.linspace(-1, 1, self.config.sim.pupilSize)
        coords = numpy.pad(
                coords, pad_width=[self.config.sim.simPad,]*2, mode="constant")
        self.tilt = numpy.meshgrid(coords, coords)[0]


    def initWfs(self, pxlScale):
        """
        Initialse a Soapy WFS with a given pixel SHPixelScale

        Paramters:
            pxlScale (float): The required pixel scale in arcsecs per pixel
        """
        self.config.wfss[0].subapFOV = (
                self.config.wfss[0].pxlsPerSubap * pxlScale)
        self.wfs = wfs.Gradient(
                self.config, mask=self.mask)

    def getSlopeFromTilt(self, tiltAmp):
        """
        applys a tilt to the WFS and find hte mean recorded tilt

        Parameters:
            tiltAmp (float): Amplitude of tilt in nm

        Returns:
            float: mean measured pixel centroid (in X direction)
        """

        aTilt = self.tilt.copy()*tiltAmp
        slopes = self.wfs.frame(aTilt)
        return -1*slopes[:self.wfs.activeSubaps].mean()


    def runTilts(self):
        """
        Runs a number of increasing tilts to be for pixel scale determination
        """
        # Must convert arcsecs of tilt to amp in nm
        self.tilts_asec = numpy.linspace(
                -MAXTILT, MAXTILT, self.nTilts)
        tilts_rad = (self.tilts_asec/3600.) * (numpy.pi/180)
        tiltAmps = 1e9 * (tilts_rad * self.config.tel.telDiam/2.)# in nm amp

        self.measuredTilts = numpy.zeros((tiltAmps.shape[0]))
        for iA, A in enumerate(tiltAmps):
            print(f"tiltAmp: {A}nm")
            self.measuredTilts[iA] = self.getSlopeFromTilt(A)

        return self.tilts_asec, self.measuredTilts


    @property
    def maxtilt(self):
        return self._maxtilt if self._maxtilt is not None else 4*self.pxlScale

    @maxtilt.setter
    def maxtilt(self, maxtilt):
        self._maxtilt = maxtilt


def testPixelScale(configfile=SOAPY_CONF):
    test = GradPixelScale(configfile=configfile)

    tiltAmps, measuredTilts = test.runTilts()

    return tiltAmps, measuredTilts
