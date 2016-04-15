"""
Makes and saves plots for the SH WFS
"""

import plotly
from plotly.graph_objs import Scatter, Layout
import os

from .. import wfs

SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")

def plotSHPixelScale(outputdir):
    if outputdir is None:
        outputdir = os.path.join(SOAPYTEST_DIR, "plots/")
    print("\nPLOT SH WFS PIXELSCALE\n***")
    ps, mps = wfs.shpixelscale.testPixelScale()

    filename = os.path.join(outputdir, 'shpixelscale.html')
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


if __name__ == '__main__':
    plotSHPixelScale()
