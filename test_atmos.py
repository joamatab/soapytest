from soapy import atmosphere, confParse

from aotools import circle
from aotools.circle import zernike

import numpy

import matplotlib.pylab as plt

def test_power_spectra(r0, N, delta, L0, l0):
    N*= 10
    phase_screen = atmosphere.ft_phase_screen(r0, N, delta, L0, l0)
    phase_screen = phase_screen[:N/10, :N/10]
    power_spec_2d = numpy.fft.fft2(phase_screen, s=(N*2, N*2))

    plt.figure()
    plt.imshow(numpy.abs(numpy.fft.fftshift(power_spec_2d)), interpolation='nearest')

    power_spec = circle.aziAvg(numpy.abs(numpy.fft.fftshift(power_spec_2d)))
    power_spec /= power_spec.sum()

    freqs = numpy.fft.fftfreq(power_spec_2d.shape[0], delta)

    print freqs

    plt.figure()
    plt.plot(freqs[:freqs.size/2], power_spec)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    return None
