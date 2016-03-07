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

def plotZernSpec():
    print("\nPLOT ATMOSPHERE ZERNIKE SPECTRUM\n***")
    noll = atmosphere.zernikepowspec.loadNoll()
    print("Test standard Soapy atmosphere")
    zCoeffs = atmosphere.zernikepowspec.getZernCoeffs()
    print("Test Sub-harmonics Soapy atmosphere")
    zCoeffs_SH = atmosphere.zernikepowspec.getZernCoeffs(subHarmonics=True)

    zVar = zCoeffs.var(1)
    zVar_SH = zCoeffs_SH.var(1)

    X = numpy.arange(1, len(zVar)+1)

    filename = os.path.join(SOAPYTEST_DIR, 'plots/atmoszernike.html')
    plotly.offline.plot(
            {   "data":[
                    Scatter(x=X, y=zVar, name="Soapy Atmosphere"),
                    Scatter(x=X, y=noll, name='Noll Theoretical',
                            line={'dash':'dash'}),
                    Scatter(x=X, y=zVar_SH, name="Soapy Atmosphere (Sub-harmonics)")],
                "layout":Layout(
                        title='Atmosphere Zernike Spectrum ($D/r^{0}=1$)',
                        xaxis={'title': 'Zernike index'},
                        yaxis={ 'type':'log',
                                'title':'Power ($rad^2$)'},
                        legend={'x':0.8, 'y':1}

                                )
            },
            auto_open=False,
            filename=filename)
