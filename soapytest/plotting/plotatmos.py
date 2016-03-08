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
