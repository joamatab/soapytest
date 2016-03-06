"""
Continuous integration tests for the soapy atmosphere module
"""

from soapytest.atmosphere import zernikepowspec

NZERNS = 50
NSCRNS = 200
SCRNSIZE = 1024
SUBSCRNSIZE = 128
R0 = 1.

import numpy

def testZernPowSpec():

    noll = zernikepowspec.loadNoll(NZERNS)
    zCoeffs = zernikepowspec.getZernCoeffs(
            NZERNS, NSCRNS, SCRNSIZE, SUBSCRNSIZE, R0)
    zVar = zCoeffs.var(1)

    # Check zernikes from phase screen match noll matrix ignoring tip/tilt
    assert numpy.allclose(zVar[2:], noll[2:], atol=5.e-3)

def testZernPowSpec_SubHarmonics():
    noll = zernikepowspec.loadNoll(NZERNS)
    zCoeffs = zernikepowspec.getZernCoeffs(
            NZERNS, NSCRNS, SCRNSIZE, SUBSCRNSIZE, R0, subHarmonics=True)
    zVar = zCoeffs.var(1)

    # Check zernikes from phase screen match noll matrix ignoring tip/tilt
    assert numpy.allclose(zVar[2:], noll[2:], atol=5.e-3)
