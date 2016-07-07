import numpy
from matplotlib import pyplot
import os
from astropy.io import fits

from soapy import atmosphere
from soapy import aoSimLib
from aotools.phasescreen import infinitephasescreen


FILEPATH = os.path.dirname(os.path.abspath(__file__))


NZERNS = 50
NSCRNS = 500
SCRNSIZE = 2**12
SUBSCRNSIZE = 512
R0 = 1.
# Always make screens of size 1metre

def testPhaseVariance(
        nScrns=NSCRNS, scrnSize=SCRNSIZE,
        subScrnSize=SUBSCRNSIZE, r0=R0, subHarmonics=False):

    subsPerScrn = int(scrnSize/subScrnSize)
    phase_var = numpy.zeros((nScrns*(subsPerScrn**2)))

    i = 0
    for n in range(nScrns):
        if n%(nScrns/10)==0:
            print("{}% complete".format(100*float(n)/nScrns))
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
                phase_var[i] = subScrn.var()
                i+=1

    return phase_var

def testPhaseVar_vs_r0(r0_range, nScrns=NSCRNS, scrnSize=SCRNSIZE,
        subScrnSize=SUBSCRNSIZE, subHarmonics=False):

    phase_vars = numpy.zeros((len(r0_range), 2))
    for i, r0 in enumerate(r0_range):
        print("\nTest R0 = {}".format(r0))
        pv = testPhaseVariance(nScrns, scrnSize, subScrnSize, r0, subHarmonics)
        phase_vars[i] = pv.mean(), pv.var()

    return phase_vars

def plot_phaseVar(r0_range, nScrns=NSCRNS, scrnSize=SCRNSIZE, subScrnSize=SUBSCRNSIZE):

    r0_range = numpy.array(r0_range)
    
    pvs = testPhaseVar_vs_r0(r0_range, nScrns, scrnSize, subScrnSize)
    pvs_sh = testPhaseVar_vs_r0(r0_range, nScrns, scrnSize, subScrnSize, subHarmonics=True)

    fig = pyplot.figure()
    pyplot.errorbar(r0_range, pvs[:, 0], yerr=pvs[:, 1], label="FT phase screen")
    pyplot.errorbar(r0_range, pvs_sh[:, 1], yerr=pvs_sh[:, 1], label="FT S-H phase screen")

    pyplot.plot(r0_range, 1.03 * (1./r0_range)**(5./3))

    pyplot.legend()

    pyplot.xlabel("r0 (m)")
    pyplot.ylabel("Variance ()")
    pyplot.show()



if __name__=="__main__":

    # Number of scrns to average over
    nScrns = 200
    r0s = numpy.array([0.05, 0.1, 0.125, 0.15, 0.175, 0.20])
    subScrnSize = 128
    scrnSize = 2048


    plot_phaseVar(r0, nScrns, scrnSize, subScrnSize)
