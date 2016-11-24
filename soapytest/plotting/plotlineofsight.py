"""
Makes and saves plots for the SH WFS
"""

import plotly
from plotly.graph_objs import Scatter, Layout
import os

from .. import lineofsight

SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")

def plotPhaseVariance(outputdir=None):
    if outputdir is None:
        outputdir = os.path.join(SOAPYTEST_DIR, "plots/")
        
    print("\nPLOT LOS PHASE VARIANCE\n***")
    phase_variance, phase_var_var = lineofsight.testphasevariance.testPhaseVariance_r0()
    
    xData = lineofsight.testphasevariance.R0_RANGE
    yData = phase_variance
    theo = 1.03 * (1./xData)**(5./3)
    

    filename = os.path.join(outputdir, 'losphasevariance.html')
    plotly.offline.plot(
            {   "data":[
                    Scatter(x=xData, y=yData, name="Soapy Line of Sight"),
                    Scatter(x=xData, y=theo, name='Theoretical', line={'dash':'dash', 'color':'black'})],
                "layout":Layout(
                        title='Line of Sight Phase Variance',
                        legend={'x':0},
                        xaxis={'title': 'Atmosphere r0 (m)'},
                        yaxis={'title': 'Measured Phase Variance (rad)'}
                        )

            },
            auto_open=False,
            filename=filename)

def plotPhaseVariance_vs_scrnSize(outputdir=None):
    if outputdir is None:
        outputdir = os.path.join(SOAPYTEST_DIR, "plots/")
        
    print("\nPLOT LOS PHASE VARIANCE vs SCRN SIZE\n***")
    phase_variance, phase_var_var = lineofsight.testphasevariance.testPhaseVariance_scrnSize()
    
    xData = lineofsight.testphasevariance.R0_RANGE
    yData = phase_variance
    theo = 1.03 * (1./xData)**(5./3)
    
    scrn_sizes= lineofsight.testphasevariance.SCRN_SIZES
    plot_list = [Scatter(x=xData, y=theo, name='Theoretical', line={'dash':'dash', 'color':'black'})]
    for i, s in enumerate(scrn_sizes):
        plot_list.append(
                Scatter(x=xData, y=yData[i], 
                name="Screen Size: {}x pupil".format(s)
                ))

    filename = os.path.join(outputdir, 'losphasevariance_vs_scrnsize.html')
    plotly.offline.plot(
            {   "data": plot_list,
                "layout":Layout(
                        title='Line of Sight Phase Variance',
                        legend={'x':0},
                        xaxis={'title': 'Atmosphere r0 (m)'},
                        yaxis={'title': 'Measured Phase Variance (rad)'}
                        )

            },
            auto_open=False,
            filename=filename)


if __name__ == '__main__':
    # plotSHPixelScale()
    plotPhaseVariance()
