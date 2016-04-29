"""
Runs tests on Soapy WFS module
"""

import numpy

from soapytest.wfs import shpixelscale

MIN_PIXELSCALE = 0.05
MAX_PIXELSCALE = 0.15

def testPixelScale():
    pxlScales, measuredPxlScales = shpixelscale.testPixelScale(
            MIN_PIXELSCALE, MAX_PIXELSCALE, nPS=10)

    print("Pixel Scales: \t\t{}".format(pxlScales))
    print("Measured Pixel Scales: \t{}".format(measuredPxlScales))

    assert numpy.allclose(pxlScales, measuredPxlScales, rtol=0.1)
