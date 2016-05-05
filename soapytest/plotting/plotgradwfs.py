"""
Makes and saves plots for the Grad WFS
"""

import plotly
from plotly.graph_objs import Scatter, Layout
import os

from .. import wfs

SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")

def plotGradPixelScale(outputdir=None):
    if outputdir is None:
        outputdir = os.path.join(SOAPYTEST_DIR, "plots/")
    print("\nPLOT Grad WFS PIXELSCALE\n***")
    ps, mps = wfs.gradpixelscale.testPixelScale()

    filename = os.path.join(outputdir, 'gradpixelscale.html')
    plotly.offline.plot(
            {   "data":[
                    Scatter(x=ps, y=mps, name="Soapy Pixel Scale"),
                    Scatter(x=ps, y=ps, name='Theoretical', line={'dash':'dash', 'color':'black'})],
                "layout":Layout(
                        title='Pixel Scale',
                        legend={'x':0})

            },
            auto_open=False,
            filename=filename)


def plotGradSlopeVariance(outputdir=None):
    if outputdir is None:
        outputdir = os.path.join(SOAPYTEST_DIR, "plots/")
        
    print("\nPLOT Grad SLOPE VARIANCE\n***")
    xData, yData = wfs.gradslopevariance.test()

    filename = os.path.join(outputdir, 'gradslopevariance.html')
    plotly.offline.plot(
            {   "data":[
                    Scatter(x=xData, y=yData, name="Soapy Grad WFS"),
                    Scatter(x=xData, y=xData, name='Theoretical', line={'dash':'dash', 'color':'black'})],
                "layout":Layout(
                        title='Grad WFS Slope Variance',
                        legend={'x':0},
                        xaxis={'title': 'Atmosphere r0'},
                        yaxis={'title': 'Measured r0'}
                        )

            },
            auto_open=False,
            filename=filename)


if __name__ == '__main__':
    plotGradPixelScale()
    plotGradSlopeVariance()
