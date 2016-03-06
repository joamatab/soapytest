"""
Runs tests on Soapy WFS module
"""

import numpy

from soapytest.wfs import shpixelscale

MIN_PS = 0.1
MAX_PS = 0.3

def testPixelScale():
    pxlScales, measuredPxlScales = shpixelscale.testPixelScale(
            MIN_PS, MAX_PS, nPS=10)

    print("Pixel Scales: \t\t{}".format(pxlScales))
    print("Measured Pixel Scales: \t{}".format(measuredPxlScales))

    assert numpy.allclose(pxlScales, measuredPxlScales, rtol=0.1)
