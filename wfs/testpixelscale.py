"""
Runs a WFS wifferent pixel scales and ensures that those set correspond with those measured.
"""
from soapy import WFS, confParse
from aotools import circle

import numpy
from matplotlib import pyplot

def getSlopes(configfile, pxlScale, tiltAngle):
    """
    Calculates the slopes recorded by a WFS with given pixel scale, for a given angle of tilt at the telescope pupil. The sub-aperture FOV is changed to
    give the desired pixel scale.

    Paramters:
        configfile (str): The soapy config file describing the telescope and WFS
        pxlScale ()

    """


    config = confParse.Configurator(configfile)
    config.loadSimParams()

    # Set the desired pxl scale by changing the subap FOV
    config.wfss[0].subapFOV = pxlScale * config.wfss[0].pxlsPerSubap

    mask = circle.circle(config.sim.pupilSize/2., config.sim.simSize)

    wfs = WFS.ShackHartmann(
            config.sim, config.wfss[0], config.atmos, mask=mask)

    # Find tilt Amplitude that gives tiltAngle
    subapDiam = config.tel.telDiam/ config.wfss[0].nxSubaps
    tiltAmp = (tiltAngle/3600.) * (numpy.pi/180.) * subapDiam/2.

    # Multiple by the number of subaps for total tilt across pupil
    tiltAmp *= config.wfss[0].nxSubaps

    # Fix for the pupil oversizing
    tiltAmp *= float(config.sim.simSize)/config.sim.pupilSize

    # Make the tilt (and tip)
    tiltCoords = numpy.linspace(-tiltAmp, tiltAmp, config.sim.simSize)
    xTilt, yTilt = numpy.meshgrid(tiltCoords, tiltCoords)

    slopes = wfs.frame(xTilt) * pxlScale

    return slopes

def getSlopeForAngle(configfile, pxlScale, angles):

    meanCents = numpy.zeros((len(angles), 2))

    for i, a in enumerate(angles):
        slopes = getSlopes(configfile, pxlScale, a)
        meanCents[i] = slopes.reshape(2, slopes.shape[0]/2.).mean(1)

    return meanCents

def testPxlScale(configfile, pxlScales, angles):

    meanCents = numpy.zeros((len(pxlScales), len(angles), 2))
    for i, p in enumerate(pxlScales):
        meanCents[i] = getSlopeForAngle(configfile, p, angles)

    return meanCents

def plotPxlScale(meanCents, pxlScales, angles):

    fig = pyplot.figure()

    for i, p in enumerate(pxlScales):
        pyplot.plot(angles, meanCents[i,:,0], label="Pixel Scale: {}".format(p))
    pyplot.legend()
    pyplot.show()

if __name__ == "__main__":
    configfile = "conf/test_conf.py"
    pxlScales = [0.1, 0.2, 0.3, 0.4]
    angles = numpy.linspace(-2, 2, 50)

    meanCents = testPxlScale(configfile, pxlScales, angles)
    plotPxlScale(meanCents, pxlScales, angles)
