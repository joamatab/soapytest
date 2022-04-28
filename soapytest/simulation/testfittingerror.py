import os

import numpy

import soapy

SOAPYTEST_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "../../")
SOAPY_CONF = os.path.join(SOAPYTEST_DIR, "conf/simulation/fittingerror.yaml")

N_SUBAPS = [4, 6, 8, 10, 14, 20, 24, 30]
RUNS = 4

class TestFittingError(soapy.Sim):

    def __init__(self, configfile=None):

        if configfile is None:
            configfile = SOAPY_CONF 
        
        super(TestFittingError, self).__init__(configfile)
        
    def test_nSubaps(self, nSubaps):
        self.config.wfss[0].nxSubaps = nSubaps
        self.config.dms[0].nxActuators = nSubaps + 1
        self.aoinit()
        self.makeIMat(forceNew=True)
        self.aoloop()

        return self.longStrehl[0, -1]

    def run_all_nSubaps(self, subap_range=None, runs=None):
        
        if subap_range is None:
            subap_range = N_SUBAPS
        if runs is None:
            runs = RUNS

        wfe_data = numpy.zeros((len(subap_range), runs))
        strehl_data = numpy.zeros((len(subap_range), runs))

        for s in subap_range:
            self.test_nSubaps(s)
        


def run_test():
    test = TestFittingError()

    test.run_all_nSubaps(N_SUBAPS, RUNS)