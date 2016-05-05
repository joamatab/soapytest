"""
Runs tests on Soapy WFS module
"""

import numpy

from soapytest.wfs import gradpixelscale


def testPixelScale():
    pxlScales, measuredPxlScales = gradpixelscale.testPixelScale()

    print("Tilts: \t\t{}".format(pxlScales))
    print("Measured Tilts: \t{}".format(measuredPxlScales))

    assert numpy.allclose(pxlScales, measuredPxlScales, rtol=0.1)
