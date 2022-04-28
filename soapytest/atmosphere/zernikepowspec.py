import os

import numpy
import plotly
from plotly.graph_objs import Scatter, Layout
from astropy.io import fits
from matplotlib import pyplot

from soapy import atmosphere
# from soapy import aoSimLib

from aotools.turbulence import infinitephasescreen
from aotools import circle, turbulence


FILEPATH = os.path.dirname(os.path.abspath(__file__))


NZERNS = 50
NSCRNS = 10
SCRNSIZE = 2**10
SUBSCRNSIZE = 64
R0 = 1.
# Always make screens of size 1metre

def getZernCoeffs(
        nZerns=NZERNS, nScrns=NSCRNS, scrnSize=SCRNSIZE,
        subScrnSize=SUBSCRNSIZE, r0=R0, subHarmonics=False):

    Zs = circle.zernikeArray(nZerns+1, subScrnSize)
    piston = Zs[0]
    Zs = Zs[1:]
    Zs.shape = nZerns, subScrnSize*subScrnSize

    subsPerScrn = int(scrnSize/subScrnSize)
    zCoeffs = numpy.zeros((nZerns, nScrns*(subsPerScrn**2)))

    i = 0
    for n in range(nScrns):
        if n%(NSCRNS/10)==0:
            print(f"{100*float(n) / NSCRNS}% complete")
        # Make one big screen
        if subHarmonics:
            scrn = turbulence.ft_sh_phase_screen(
                    r0, scrnSize, 1./subScrnSize, 100., 0.01)
        else:
            scrn = turbulence.ft_phase_screen(
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

def getZernCoeffs_infinite(
        nZerns=NZERNS, nScrns=NSCRNS, subScrnSize=SUBSCRNSIZE, r0=R0):

    scrn = infinitephasescreen.PhaseScreen(subScrnSize, 10./subScrnSize, r0, L0=100, nCol=4)

    Zs = circle.zernikeArray(nZerns+1, subScrnSize)
    piston = Zs[0]
    Zs = Zs[1:]
    Zs.shape = nZerns, subScrnSize*subScrnSize

    zCoeffs = numpy.zeros((nZerns, nScrns))
    for i in range(nScrns):
        if i % (nScrns / 10) == 0:
            print(f"{100 * float(i) / nScrns}% complete")
        scrn.addRow(subScrnSize)

        subScrn = scrn.scrn.copy().reshape(subScrnSize*subScrnSize)

        zCoeffs[:, i] = (Zs*subScrn).sum(1)/piston.sum()

    return zCoeffs

def loadNoll(nZerns=NZERNS):
    """
    Loads the noll reference values for Zernike variance in Kolmogorov turbulence.
    """
    nollPath = os.path.join(FILEPATH, "../../resources/noll.fits")
    noll = fits.getdata(nollPath)

    return noll.diagonal()[:nZerns]


def plotZernSpec_mpl(zvar, noll, filename=None, show=False):

    pyplot.figure()

    pyplot.semilogy(noll, label="Noll reference", color="k", linestyle="--")

    for label, var in zvar.items():
        pyplot.semilogy(var, label=label)

    pyplot.xlabel("Zernike mode index")
    pyplot.ylabel("Power ($rad^2$)")

    pyplot.legend(loc=0)

    if filename!=None:
        pyplot.savefig(filename)
    if show:
        pyplot.show()


def plotZernSpec(zvar, noll, outputdir='plots'):

    X = numpy.arange(1, len(noll)+1)

    filename = os.path.join(outputdir, 'atmoszernike.html')
    plots = [Scatter(x=X, y=var, name=label) for (label, var) in zvar.items()]
    plots.append(Scatter(x=X, y=noll, name='Noll theoretical',
                            line={'dash':'dash', 'color':'black'}))
    print(plots)
    plotly.offline.plot(
            {   "data": plots,
                "layout": Layout(
                        xaxis={'title': 'Zernike Index'},
                        yaxis={ 'type':'log',
                                'title':'Power (rad^2)'
                                },
                        legend={'x':0.6, 'y':0.9}
                        )
            },
            auto_open=False,
            filename=filename)

def run_test(no_sh=True, sh=True, infinite=True, plotmpl=False, plotplotly=True):

    print("\nPLOT ATMOSPHERE ZERNIKE SPECTRUM\n***")
    noll = loadNoll(NZERNS)

    zCoeffs = {}
    if no_sh:
        print("Test standard Soapy atmosphere")
        zCoeffs["AOtools Phase Screens"] = getZernCoeffs()

    if sh:
        print("Test Sub-harmonics Soapy atmosphere")
        zCoeffs["AOtools Phase Screens + Subharmonics"] = getZernCoeffs(subHarmonics=True)

    if infinite:
        print("Test infinite Phase screens")
        zCoeffs["AOtools Infinite Phase Screens"] = getZernCoeffs_infinite()

    zvar = {key: value.var(1) for (key, value) in zCoeffs.items()}

    if plotmpl:
        print("Show matplotlib plot")
        plotZernSpec_mpl(zvar, noll, show=True)

    if plotplotly:
        print("Create plotly plot")
        plotZernSpec(zvar, noll, os.path.join(FILEPATH, '../../plots/'))



if __name__=="__main__":

    run_test(plotmpl=True, infinite=True)