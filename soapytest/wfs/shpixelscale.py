import numpy

from soapy import confParse, wfs
import aotools

import os
SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")
SOAPY_CONF = os.path.join(SOAPYTEST_DIR, "conf/wfs/shpixelscale.yaml")


MIN_PIXELSCALE = 0.02
# This is just larger than the diffraction limit
MAX_PIXELSCALE = 0.15


class SHPixelScale(object):
    def __init__(self, configfile=SOAPY_CONF):

        self.configfile = configfile
        self.loadConfig()

        self.makeTilt()

        self.maxtilt = None
        self.pxlScale = (
                float(self.config.wfss[0].subapFOV)
                /self.config.wfss[0].pxlsPerSubap)
        self.nTilts = 10

    def loadConfig(self):
        """
        Load the Soapy config file
        """
        self.config = confParse.YAML_Configurator(self.configfile)
        self.config.loadSimParams()

        self.mask = aotools.circle(
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
        self.wfs = wfs.ShackHartmann(
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
        return -1*slopes[self.wfs.activeSubaps:].mean()


    def runTilts(self):
        """
        Runs a number of increasing tilts to be for pixel scale determination
        """
        # Must convert arcsecs of tilt to amp in nm
        self.tilts_asec = numpy.linspace(
                -self.maxtilt, self.maxtilt, self.nTilts)
        tilts_rad = (self.tilts_asec/3600.) * (numpy.pi/180)
        tiltAmps = 1e9 * (tilts_rad * self.config.tel.telDiam/2.)# in nm amp

        self.measuredTilts = numpy.zeros((tiltAmps.shape[0]))
        for iA, A in enumerate(tiltAmps):
            self.measuredTilts[iA] = self.getSlopeFromTilt(A)

    def measurePxlScale(self, pxlScale):
        """
        Measure the pixel scale by running increasing tilts and using a linear fit on the resulting slopes.
        """
        self.pxlScale = pxlScale

        self.runTilts()

        A = numpy.vstack([self.tilts_asec, numpy.ones(len(self.tilts_asec))]).T
        pxlScale, bias = numpy.linalg.lstsq(A, self.measuredTilts)[0]

        pxlScale = pxlScale**(-1.)

        return pxlScale, bias

    def testPxlScale(self, minPS, maxPS, nPS=10):
        """
        Tests various pixels scales
        """

        pxlScales = numpy.linspace(minPS, maxPS, nPS)
        print(f"Test pixel scales: {pxlScales}")
        measuredPxlScales = numpy.zeros_like(pxlScales)
        for ips, ps in enumerate(pxlScales):
            print(f"test pixel scale:{ps}")
            measuredPxlScales[ips] = self.measurePxlScale(ps)[0]

        return pxlScales, measuredPxlScales

    @property
    def pxlScale(self):
        return self._pxlScale

    @pxlScale.setter
    def pxlScale(self, pxlScale):
        self.initWfs(pxlScale)
        self._pxlScale = pxlScale

    @property
    def maxtilt(self):
        return self._maxtilt if self._maxtilt is not None else 4*self.pxlScale

    @maxtilt.setter
    def maxtilt(self, maxtilt):
        self._maxtilt = maxtilt


def testPixelScale(
        minPS=MIN_PIXELSCALE, maxPS=MAX_PIXELSCALE, configfile=SOAPY_CONF,
        nPS=10):
    test = SHPixelScale(configfile=configfile)
    pxlScales, measuredPxlScales = test.testPxlScale(minPS, maxPS, nPS)

    return pxlScales, measuredPxlScales
