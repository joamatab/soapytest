"""
Makes and saves plots for the SH WFS
"""

import plotly
from plotly.graph_objs import Scatter, Layout
import os
import numpy

from .. import atmosphere

SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")

def plotZernSpec(outputdir=None):
    if outputdir is None:
        outputdir = os.path.join(SOAPYTEST_DIR, "plots/")
    print("\nPLOT ATMOSPHERE ZERNIKE SPECTRUM\n***")
    noll = atmosphere.zernikepowspec.loadNoll()
    print("Test standard Soapy atmosphere")
    zCoeffs = atmosphere.zernikepowspec.getZernCoeffs()
    print("Test Sub-harmonics Soapy atmosphere")
    zCoeffs_SH = atmosphere.zernikepowspec.getZernCoeffs(subHarmonics=True)

    zVar = zCoeffs.var(1)
    zVar_SH = zCoeffs_SH.var(1)

    X = numpy.arange(1, len(zVar)+1)

    filename = os.path.join(outputdir, 'atmoszernike.html')
    plotly.offline.plot(
            {   "data":[
                    Scatter(x=X, y=zVar, name='Soapy atmosphere'),
                    Scatter(x=X, y=zVar_SH, name='Soapy atmosphere with Sub-harmonics'),
                    Scatter(x=X, y=noll, name='Noll theoretical',
                            line={'dash':'dash', 'color':'black'})
                            ],
                "layout":Layout(
                        xaxis={'title': 'Zernike Index'},
                        yaxis={ 'type':'log',
                                'title':'Power (rad^2)'
                                },
                        legend={'x':0.6, 'y':0.9}
                        )
            },
            auto_open=False,
            filename=filename)

def plotPhaseVariance(outputdir=None):
    if outputdir is None:
        outputdir = os.path.join(SOAPYTEST_DIR, "plots/")
    print("\nPLOT ATMOSPHERE PHASE VARIANCE\n***")

    print("Test standard Soapy atmosphere")
    phase_var = atmosphere.testphasevariance.testPhaseVar_vs_r0()
    print("Test Sub-harmonics Soapy atmosphere")
    phase_var_sh = atmosphere.testphasevariance.testPhaseVar_vs_r0(subHarmonics=True)

    X = atmosphere.testphasevariance.R0_RANGE
    theo = 1.03 * (atmosphere.testphasevariance.D/X)**(5./3)

    filename = os.path.join(outputdir, 'atmosphasevar.html')
    plotly.offline.plot(
            {   "data":[
                    Scatter(x=X, y=phase_var[:, 0], name='Soapy atmosphere'),
                    Scatter(x=X, y=phase_var_sh[:, 0], name='Soapy atmosphere with Sub-harmonics'),
                    Scatter(x=X, y=theo, name='Theoretical',
                            line={'dash':'dash', 'color':'black'})
                            ],
                "layout":Layout(
                        xaxis={'title': 'R0'},
                        yaxis={'title':'Variance (rad^2)'
                                },
                        # legend={'x':0.6, 'y':0.9}
                        )
            },
            auto_open=False,
            filename=filename)